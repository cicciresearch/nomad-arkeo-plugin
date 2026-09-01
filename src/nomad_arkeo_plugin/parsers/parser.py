from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from nomad.parsing.parser import MatchingParser
from nomad_arkeo_plugin.schema_packages.schema_package import (
    ArkeoCellSettings,
    ArkeoChannelSettings,
    ArkeoEnvironmentSettings,
    ArkeoInstrument,
    ArkeoJVResult,
    ArkeoJVSettings,
    ArkeoStabilityMeasurement,
    ArkeoStabilitySummary,
    ArkeoTrackingResult,
    ArkeoTrackingSettings,
)
from .text_reader import (
    ARKEO_FILENAME_RE,
    decode_arkeo_bytes,
    is_arkeo_stability_parameters,
    parse_stability_measurement,
)

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import EntryArchive
    from structlog.stdlib import BoundLogger


def _finite(value):
    return value is not None and not (isinstance(value, float) and math.isnan(value))


def _array(values):
    return np.asarray(values or [], dtype=float)


def _read_bytes(archive: "EntryArchive", filename: str) -> bytes:
    try:
        with archive.m_context.raw_file(filename, mode="rb") as handle:
            return handle.read()
    except Exception:
        with open(filename, "rb") as handle:
            return handle.read()


def _seconds(value):
    h, m, s = (int(part) for part in value.split("."))
    return h * 3600 + m * 60 + s


def _candidate_auxiliary(mainfile: str, kind: str, device: str | None):
    parent = Path(mainfile).parent
    if not parent.exists():
        return None
    main_match = ARKEO_FILENAME_RE.match(Path(mainfile).name)
    candidates = []
    for path in parent.iterdir():
        if not path.is_file():
            continue
        match = ARKEO_FILENAME_RE.match(path.name)
        if not match or match.group("kind").lower() != kind.lower():
            continue
        if device and match.group("sample").lower() != device.lower():
            continue
        candidates.append((path, match))
    if not candidates:
        return None
    if main_match:
        base = _seconds(main_match.group("time"))
        candidates.sort(key=lambda item: abs(_seconds(item[1].group("time")) - base))
    return str(candidates[0][0])


class ArkeoStabilityParser(MatchingParser):
    def __init__(self):
        super().__init__(name="arkeo_stability_parser")

    def is_mainfile(
        self,
        filename,
        mime=None,
        buffer=None,
        decoded_buffer=None,
        compression=None,
    ):
        if not ARKEO_FILENAME_RE.match(Path(filename).name):
            return False
        try:
            text = decoded_buffer
            if not text:
                text = decode_arkeo_bytes(buffer) if buffer else decode_arkeo_bytes(Path(filename).read_bytes())
        except Exception:
            return False
        return is_arkeo_stability_parameters(filename, text)

    def parse(self, mainfile, archive, logger, child_archives=None):
        main_text = decode_arkeo_bytes(_read_bytes(archive, mainfile))
        initial = parse_stability_measurement(main_text)
        device = initial["parameters"]["general"].get("device")

        tracking_file = _candidate_auxiliary(mainfile, "Tracking", device)
        jv_file = _candidate_auxiliary(mainfile, "JV", device)
        tracking_text = decode_arkeo_bytes(_read_bytes(archive, tracking_file)) if tracking_file else None
        jv_text = decode_arkeo_bytes(_read_bytes(archive, jv_file)) if jv_file else None
        parsed = parse_stability_measurement(main_text, tracking_text, jv_text)
        p = parsed["parameters"]

        measurement = ArkeoStabilityMeasurement()
        general = p["general"]
        measurement.user = general.get("user")
        measurement.note = general.get("note")
        if general.get("measurement_start"):
            measurement.measurement_start = general["measurement_start"]
        measurement.source_files = [Path(mainfile).name] + (
            [Path(tracking_file).name] if tracking_file else []
        ) + ([Path(jv_file).name] if jv_file else [])

        instrument = ArkeoInstrument()
        for key, value in p["instrument"].items():
            if value:
                setattr(instrument, key, value)
        measurement.instrument = instrument

        channel = ArkeoChannelSettings()
        if _finite(p["channel"]["voltage_range_v"]):
            channel.voltage_range = p["channel"]["voltage_range_v"]
        if p["channel"].get("current_range_label"):
            channel.current_range_label = p["channel"]["current_range_label"]
        measurement.channel_settings = channel

        cell = ArkeoCellSettings()
        if general.get("device"):
            cell.device_id = general["device"]
        if p["cell"].get("device_type"):
            cell.device_type = p["cell"]["device_type"]
        area = p["cell"]["cell_area_cm2"]
        if not _finite(area):
            area = general["cell_area_cm2"]
        if _finite(area):
            cell.cell_area = area
        if p["cell"].get("inverted") is not None:
            cell.inverted = p["cell"]["inverted"]
        if p["cell"].get("number_of_cells") is not None:
            cell.number_of_cells = p["cell"]["number_of_cells"]
        measurement.cell = cell

        environment = ArkeoEnvironmentSettings()
        if _finite(p["environment"]["irradiance_mw_cm2"]):
            environment.irradiance = p["environment"]["irradiance_mw_cm2"]
        measurement.environment = environment

        jvs = ArkeoJVSettings()
        for src, dst in {
            "vmin_v": "vmin", "vmax_v": "vmax", "voltage_step_mv": "voltage_step",
            "scan_rate_mv_s": "scan_rate", "scan_order": "scan_order",
            "auto_detect_voc": "auto_detect_voc", "overvoltage_percent": "overvoltage_percent",
        }.items():
            value = p["jv_settings"].get(src)
            if value is not None and not (isinstance(value, float) and math.isnan(value)):
                setattr(jvs, dst, value)
        measurement.jv_settings = jvs

        summary = ArkeoStabilitySummary()
        for src, dst in {
            "time_hours": "time_hours", "voc_fw": "voc_fw", "jsc_fw": "jsc_fw",
            "v_mpp_fw": "v_mpp_fw", "j_mpp_fw": "j_mpp_fw", "p_mpp_fw": "p_mpp_fw",
            "rs_fw": "series_resistance_fw", "rsh_fw": "shunt_resistance_fw",
            "ff_fw": "fill_factor_fw", "eff_fw": "efficiency_fw", "voc_rv": "voc_rv",
            "jsc_rv": "jsc_rv", "v_mpp_rv": "v_mpp_rv", "j_mpp_rv": "j_mpp_rv",
            "p_mpp_rv": "p_mpp_rv", "rs_rv": "series_resistance_rv",
            "rsh_rv": "shunt_resistance_rv", "ff_rv": "fill_factor_rv",
            "eff_rv": "efficiency_rv",
        }.items():
            setattr(summary, dst, _array(p["summary"][src]))
        measurement.stability_summary = summary

        if "tracking" in parsed:
            t = parsed["tracking"]
            settings = ArkeoTrackingSettings()
            for src, dst in {
                "algorithm": "algorithm", "jv_timing": "jv_timing",
                "jv_interval_hours": "jv_interval", "test_duration_hours": "test_duration",
                "startup_time_raw": "startup_time_raw", "min_dv_v": "min_dv",
            }.items():
                value = t["settings"].get(src)
                if value is not None and not (isinstance(value, float) and math.isnan(value)):
                    setattr(settings, dst, value)
            measurement.tracking_settings = settings

            r = t["result"]
            tracking = ArkeoTrackingResult()
            tracking.time_axis_kind = r.get("time_axis_kind")
            tracking.time_hours = _array(r["time_hours"])
            tracking.timestamp_text = r["timestamp_text"]
            tracking.voltage = _array(r["voltage_v"])
            tracking.current_density = _array(r["current_density_ma_cm2"])
            tracking.power_density = _array(r["power_density_mw_cm2"])
            measurement.tracking_result = tracking

        if "jv" in parsed:
            results = []
            for name in ("forward", "reverse"):
                d = parsed["jv"][name]
                result = ArkeoJVResult()
                result.direction = d["direction"]
                for src, dst in {
                    "voc_v": "voc", "jsc_a_cm2": "jsc", "v_mpp_v": "v_mpp",
                    "j_mpp_a_cm2": "j_mpp", "p_mpp_w_cm2": "p_mpp",
                    "series_resistance_ohm": "series_resistance",
                    "shunt_resistance_ohm": "shunt_resistance",
                    "fill_factor_percent": "fill_factor_percent",
                    "efficiency_percent": "efficiency_percent",
                }.items():
                    if _finite(d[src]):
                        setattr(result, dst, d[src])
                result.voltage = _array(d["voltage_v"])
                result.current_density = _array(d["current_density_a_cm2"])
                results.append(result)
            measurement.jv_results = results

        archive.data = measurement
        if getattr(archive, "metadata", None) is not None:
            device_name = general.get("device") or "unknown sample"
            dt = general.get("measurement_start")
            time_text = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else ""
            archive.metadata.entry_name = f"ARKEO Stability - {device_name} - {time_text}".strip()

        logger.info(
            "Parsed ARKEO Stability measurement",
            mainfile=mainfile,
            tracking_file=tracking_file,
            jv_file=jv_file,
            device=device,
        )

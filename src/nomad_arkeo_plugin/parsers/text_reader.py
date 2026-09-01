from __future__ import annotations

import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

ARKEO_FILENAME_RE = re.compile(
    r"^(?P<index>\d{4})_(?P<date>\d{4}-\d{2}-\d{2})_"
    r"(?P<time>\d{2}\.\d{2}\.\d{2})_Stability "
    r"\((?P<kind>Parameters|Tracking|JV)\)_(?P<sample>.+)\.txt$",
    re.IGNORECASE,
)

REQUIRED_MAINFILE_MARKERS = (
    "[General info]",
    "[Channel Settings]",
    "[Cell Settings]",
    "[JV Settings]",
    "[Environment Settings]",
    "Stability (Parameters)",
)


def decode_arkeo_bytes(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return clean_text(raw.decode(encoding, errors="strict"))
        except UnicodeDecodeError:
            pass
    return clean_text(raw.decode("utf-8", errors="replace"))


def clean_text(text: str) -> str:
    return (
        text.replace("\ufeff", "")
        .replace("Â²", "²")
        .replace("cm▓", "cm²")
        .replace("cm�", "cm²")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def is_arkeo_stability_parameters(filename: str, text: str) -> bool:
    match = ARKEO_FILENAME_RE.match(Path(filename).name)
    if not match or match.group("kind").lower() != "parameters":
        return False
    clean = clean_text(text)
    return all(marker in clean for marker in REQUIRED_MAINFILE_MARKERS)


def _split_document(text: str) -> dict[str, dict[str, Any]]:
    text = clean_text(text)
    blocks: dict[str, dict[str, Any]] = {}
    current_block = None
    current_section = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        marker = re.fullmatch(r"\s*##\s*(.*?)\s*##\s*", line)
        if marker:
            current_block = marker.group(1).strip()
            blocks.setdefault(current_block, {"sections": {}, "lines": []})
            current_section = None
            continue

        section = re.fullmatch(r"\s*\[(.*?)\]\s*", line)
        if section and current_block:
            current_section = section.group(1).strip()
            blocks[current_block]["sections"].setdefault(current_section, {})
            continue

        if not current_block:
            continue

        if current_section and "\t" in line:
            key, value = line.split("\t", 1)
            blocks[current_block]["sections"][current_section][key.strip()] = value.strip()
        else:
            blocks[current_block]["lines"].append(line)

    return blocks


def _table(lines: list[str]) -> tuple[list[str], list[dict[str, str]]]:
    nonempty = [line for line in lines if line.strip()]
    if not nonempty:
        return [], []
    headers = [h.strip() for h in nonempty[0].split("\t")]
    rows = []
    for line in nonempty[1:]:
        cells = line.split("\t")
        cells += [""] * max(0, len(headers) - len(cells))
        rows.append({headers[i]: cells[i].strip() for i in range(len(headers))})
    return headers, rows


def _float(value: str | None) -> float:
    if value is None:
        return math.nan
    value = value.strip()
    if not value or value.lower() == "nan":
        return math.nan
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return math.nan


def _bool(value: str | None) -> bool | None:
    if value is None:
        return None
    value = value.strip().lower()
    if value in {"yes", "true", "1"}:
        return True
    if value in {"no", "false", "0"}:
        return False
    return None


def _datetime(date: str | None, time: str | None) -> datetime | None:
    if not date or not time:
        return None
    try:
        return datetime.strptime(f"{date.strip()} {time.strip()}", "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _section(blocks, block, section):
    return blocks.get(block, {}).get("sections", {}).get(section, {})


def _first(row, *keys):
    for key in keys:
        if key in row:
            return _float(row[key])
    return math.nan


def parse_parameters(text: str) -> dict[str, Any]:
    blocks = _split_document(text)
    general = _section(blocks, "Header", "General info")
    channel = _section(blocks, "Header", "Channel Settings")
    cell = _section(blocks, "Header", "Cell Settings")
    jv = _section(blocks, "Header", "JV Settings")
    env = _section(blocks, "Header", "Environment Settings")
    instrument = _section(blocks, "Header", "Instrument")
    _, rows = _table(blocks.get("Data", {}).get("lines", []))

    names = [
        "time_hours", "voc_fw", "jsc_fw", "v_mpp_fw", "j_mpp_fw", "p_mpp_fw",
        "rs_fw", "rsh_fw", "ff_fw", "eff_fw", "voc_rv", "jsc_rv", "v_mpp_rv",
        "j_mpp_rv", "p_mpp_rv", "rs_rv", "rsh_rv", "ff_rv", "eff_rv",
    ]
    summary = {name: [] for name in names}

    for row in rows:
        values = {
            "time_hours": _first(row, "Time (Hours)"),
            "voc_fw": _first(row, "Voc (V) FW"),
            "jsc_fw": _first(row, "Jsc (mA/cm2) FW", "Jsc (mA/cm²) FW"),
            "v_mpp_fw": _first(row, "V_MPP (V) FW"),
            "j_mpp_fw": _first(row, "J_MPP (mA/cm2) FW", "J_MPP (mA/cm²) FW"),
            "p_mpp_fw": _first(row, "P_MPP (mW/cm2) FW", "P_MPP (mW/cm²) FW"),
            "rs_fw": _first(row, "Rs (Ohm) FW"),
            "rsh_fw": _first(row, "R// (Ohm) FW"),
            "ff_fw": _first(row, "Fill Factor (%) FW"),
            "eff_fw": _first(row, "Efficiency (%) FW"),
            "voc_rv": _first(row, "Voc (V) RV"),
            "jsc_rv": _first(row, "Jsc (mA/cm2) RV", "Jsc (mA/cm²) RV"),
            "v_mpp_rv": _first(row, "V_MPP (V) RV"),
            "j_mpp_rv": _first(row, "J_MPP (mA/cm2) RV", "J_MPP (mA/cm²) RV"),
            "p_mpp_rv": _first(row, "P_MPP (mW/cm2) RV", "P_MPP (mW/cm²) RV"),
            "rs_rv": _first(row, "Rs (Ohm) RV"),
            "rsh_rv": _first(row, "R// (Ohm) RV"),
            "ff_rv": _first(row, "Fill Factor (%) RV"),
            "eff_rv": _first(row, "Efficiency (%) RV"),
        }
        for key, value in values.items():
            summary[key].append(value)

    n_cells = _float(cell.get("#Cells"))
    return {
        "general": {
            "user": general.get("User"),
            "device": general.get("Device"),
            "cell_area_cm2": _float(general.get("Cell area (cm2)")),
            "test": general.get("Test"),
            "date": general.get("Date"),
            "time": general.get("Time"),
            "measurement_start": _datetime(general.get("Date"), general.get("Time")),
            "note": general.get("Note"),
        },
        "instrument": {
            "manufacturer": instrument.get("Manufacturer") or "CICCI Research",
            "product": instrument.get("Product") or "ARKEO",
            "model": instrument.get("Model"),
            "serial_number": instrument.get("Serial Number"),
            "software": instrument.get("Software"),
            "software_version": instrument.get("Software Version"),
            "data_format_version": instrument.get("Data Format"),
            "identification_method": (
                "explicit [Instrument] metadata"
                if instrument
                else "inferred from CICCI ARKEO Stability TXT signature"
            ),
        },
        "channel": {
            "voltage_range_v": _float(channel.get("Voltage Range", "").replace(" V", "")),
            "current_range_label": channel.get("Current Range"),
        },
        "cell": {
            "inverted": _bool(cell.get("Inverted")),
            "device_type": cell.get("Type"),
            "cell_area_cm2": _float(cell.get("Cell Area (cm2)")),
            "number_of_cells": int(n_cells) if not math.isnan(n_cells) else None,
        },
        "jv_settings": {
            "vmin_v": _float(jv.get("Vmin (V)")),
            "vmax_v": _float(jv.get("Vmax (V)")),
            "voltage_step_mv": _float(jv.get("Voltage Step (mV)")),
            "scan_rate_mv_s": _float(jv.get("Scan Rate (mV/s)")),
            "scan_order": jv.get("Scan Order"),
            "auto_detect_voc": _bool(jv.get("Auto-detect Voc")),
            "overvoltage_percent": _float(jv.get("Overvoltage (%)")),
        },
        "environment": {
            "irradiance_mw_cm2": _float(
                env.get("Irradiance (mW/cm²)") or env.get("Irradiance (mW/cm2)")
            )
        },
        "summary": summary,
    }


def parse_tracking(text: str) -> dict[str, Any]:
    blocks = _split_document(text)
    settings = _section(blocks, "Header", "Tracking Settings")
    env = _section(blocks, "Header", "Environment Settings")
    _, rows = _table(blocks.get("Data", {}).get("lines", []))
    result = {
        "time_axis_kind": None, "time_hours": [], "timestamp_text": [],
        "voltage_v": [], "current_density_ma_cm2": [], "power_density_mw_cm2": [],
    }
    for row in rows:
        raw_time = row.get("Time (Hours)", "")
        numeric = _float(raw_time)
        if not math.isnan(numeric):
            result["time_axis_kind"] = result["time_axis_kind"] or "relative_hours"
            result["time_hours"].append(numeric)
            result["timestamp_text"].append("")
        else:
            result["time_axis_kind"] = "timestamp_text"
            result["time_hours"].append(math.nan)
            result["timestamp_text"].append(raw_time)
        result["voltage_v"].append(_first(row, "Voltage (V)"))
        result["current_density_ma_cm2"].append(
            _first(row, "Current Density (mA/cm²)", "Current Density (mA/cm2)")
        )
        result["power_density_mw_cm2"].append(
            _first(row, "Power (mW/cm²)", "Power (mW/cm2)")
        )

    return {
        "settings": {
            "algorithm": settings.get("Algorithm"),
            "jv_timing": settings.get("JV Timing"),
            "jv_interval_hours": _float(settings.get("JV interval (hours)")),
            "test_duration_hours": _float(settings.get("Test duration (hours)")),
            "startup_time_raw": settings.get("Start-up Time"),
            "min_dv_v": _float(settings.get("min dV (V)")),
        },
        "environment": {
            "irradiance_mw_cm2": _float(
                env.get("Irradiance (mW/cm²)") or env.get("Irradiance (mW/cm2)")
            )
        },
        "result": result,
    }


def parse_jv(text: str) -> dict[str, Any]:
    blocks = _split_document(text)
    forward = _section(blocks, "Parameters", "Forward")
    reverse = _section(blocks, "Parameters", "Reverse")
    _, rows = _table(blocks.get("Data", {}).get("lines", []))

    def make(values, direction):
        return {
            "direction": direction,
            "voc_v": _float(values.get("Voc (V)")),
            "jsc_a_cm2": _float(values.get("Jsc (A/cm²)") or values.get("Jsc (A/cm2)")),
            "v_mpp_v": _float(values.get("V_MPP (V)")),
            "j_mpp_a_cm2": _float(values.get("J_MPP (A/cm²)") or values.get("J_MPP (A/cm2)")),
            "p_mpp_w_cm2": _float(values.get("P_MPP (W/cm²)") or values.get("P_MPP (W/cm2)")),
            "series_resistance_ohm": _float(values.get("Rs (Ohm)")),
            "shunt_resistance_ohm": _float(values.get("R// (Ohm)")),
            "fill_factor_percent": _float(values.get("FF (%)")),
            "efficiency_percent": _float(values.get("Eff (%)")),
            "voltage_v": [],
            "current_density_a_cm2": [],
        }

    fw, rv = make(forward, "Forward"), make(reverse, "Reverse")
    for row in rows:
        v, j = _first(row, "V_FW (V)"), _first(row, "J_FW (A/cm²)", "J_FW (A/cm2)")
        if not math.isnan(v) and not math.isnan(j):
            fw["voltage_v"].append(v)
            fw["current_density_a_cm2"].append(j)
        v, j = _first(row, "V_RV (V)"), _first(row, "J_RV (A/cm²)", "J_RV (A/cm2)")
        if not math.isnan(v) and not math.isnan(j):
            rv["voltage_v"].append(v)
            rv["current_density_a_cm2"].append(j)
    return {"forward": fw, "reverse": rv}


def parse_stability_measurement(parameters_text, tracking_text=None, jv_text=None):
    result = {"parameters": parse_parameters(parameters_text)}
    if tracking_text:
        result["tracking"] = parse_tracking(tracking_text)
    if jv_text:
        result["jv"] = parse_jv(jv_text)
    return result

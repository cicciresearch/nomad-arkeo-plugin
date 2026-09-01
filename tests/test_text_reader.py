from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from nomad_arkeo_plugin.parsers.text_reader import (  # noqa: E402
    is_arkeo_stability_parameters,
    parse_jv,
    parse_parameters,
    parse_stability_measurement,
    parse_tracking,
)

EXAMPLE = ROOT / "src/nomad_arkeo_plugin/example_uploads/getting_started"
PARAMETERS = "0000_2026-01-01_12.00.00_Stability (Parameters)_Demo-Cell-01.txt"
TRACKING = "0000_2026-01-01_12.00.00_Stability (Tracking)_Demo-Cell-01.txt"
JV = "0001_2026-01-01_12.00.04_Stability (JV)_Demo-Cell-01.txt"


def text(name):
    return (EXAMPLE / name).read_text(encoding="utf-8")


def test_mainfile():
    assert is_arkeo_stability_parameters(PARAMETERS, text(PARAMETERS))
    assert not is_arkeo_stability_parameters(TRACKING, text(TRACKING))


def test_parameters():
    p = parse_parameters(text(PARAMETERS))
    assert p["general"]["device"] == "Demo-Cell-01"
    assert p["instrument"]["manufacturer"] == "CICCI Research"
    assert p["instrument"]["product"] == "ARKEO"
    assert p["cell"]["inverted"] is True
    assert p["environment"]["irradiance_mw_cm2"] == 100.0
    assert p["summary"]["voc_fw"][0] == -0.67423398


def test_tracking():
    t = parse_tracking(text(TRACKING))
    assert t["settings"]["algorithm"] == "MPPT"
    assert t["settings"]["test_duration_hours"] == 100.0
    assert len(t["result"]["voltage_v"]) == 3


def test_jv():
    jv = parse_jv(text(JV))
    assert jv["forward"]["voc_v"] == -0.67604
    assert jv["forward"]["series_resistance_ohm"] == 8860.0
    assert len(jv["forward"]["voltage_v"]) == 4
    assert len(jv["reverse"]["voltage_v"]) == 1
    assert math.isnan(jv["reverse"]["series_resistance_ohm"])


def test_full():
    result = parse_stability_measurement(text(PARAMETERS), text(TRACKING), text(JV))
    assert set(result) == {"parameters", "tracking", "jv"}

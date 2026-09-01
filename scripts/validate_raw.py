from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from nomad_arkeo_plugin.parsers.text_reader import parse_stability_measurement  # noqa: E402


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace") if path else None


parser = argparse.ArgumentParser()
parser.add_argument("parameters")
parser.add_argument("--tracking")
parser.add_argument("--jv")
args = parser.parse_args()
print(
    json.dumps(
        parse_stability_measurement(read(args.parameters), read(args.tracking), read(args.jv)),
        indent=2,
        default=str,
        allow_nan=True,
    )
)

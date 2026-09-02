# ARKEO NOMAD Plugin

NOMAD plugin for **CICCI Research ARKEO** photovoltaic measurement data.

The plugin allows NOMAD Oasis to recognize original ARKEO measurement files and convert them into structured, searchable research data.

## Features

- Automatic parsing of supported ARKEO TXT files
- Structured ARKEO measurement entries
- Instrument and device metadata
- JV and stability results
- Dedicated **ARKEO Explorer**
- Compatible with private NOMAD Oasis installations

## Supported measurements

Version **0.1.0** currently supports ARKEO Stability measurements:

- Stability (Parameters)
- Stability (Tracking)
- Stability (JV)

The Parameters file is recognized as the main file. Associated Tracking and JV files in the same folder are processed automatically.

## Workflow

ARKEO measurement  
→ Original TXT files  
→ ARKEO NOMAD Plugin  
→ Structured NOMAD entry  
→ Search, compare, share or publish

No manually created `.archive.yaml` file is required for supported ARKEO files.

## ARKEO Explorer

After installation, NOMAD provides:

`EXPLORE → ARKEO`

The dedicated interface can be used to search and filter ARKEO measurements using structured metadata and results.

## Requirements

- NOMAD `>=1.4.3,<1.5`
- Python `>=3.10`
- NOMAD Oasis for local or institutional deployment

Current development target: **NOMAD 1.4.3**.

## Documentation

Full documentation is available at:

https://cicciresearch.github.io/nomad-arkeo-plugin/

- [Installation guide](https://cicciresearch.github.io/nomad-arkeo-plugin/how_to/install_this_plugin/)
- [How to use](https://cicciresearch.github.io/nomad-arkeo-plugin/how_to/use_this_plugin/)
- [Support](https://cicciresearch.github.io/nomad-arkeo-plugin/support/)
- [Release v0.1.0](https://github.com/cicciresearch/nomad-arkeo-plugin/releases/tag/v0.1.0)

## Installation

Clone the plugin with:

```bash
git clone --branch v0.1.0 --depth 1 https://github.com/cicciresearch/nomad-arkeo-plugin.git
```

Then follow the [installation guide](https://cicciresearch.github.io/nomad-arkeo-plugin/how_to/install_this_plugin/).

## Usage

Upload the original ARKEO TXT files belonging to the same measurement to NOMAD Oasis.

For a Stability measurement, this normally includes:

```text
Stability (Parameters)
Stability (Tracking)
Stability (JV)
```

The plugin processes the files automatically and creates a structured ARKEO entry.

Use:

`EXPLORE → ARKEO`

to search and filter processed measurements.

See the full [usage guide](https://cicciresearch.github.io/nomad-arkeo-plugin/how_to/use_this_plugin/).

The example files included in this repository are intended only for demonstration and testing.

## Privacy

The plugin does not automatically publish research data.

Data uploaded to NOMAD Oasis remain subject to the privacy, sharing, and publication settings of the institution's NOMAD installation.

## Support

For assistance with installation, NOMAD Oasis integration, or ARKEO data compatibility, contact:

**support@cicciresearch.com**

Please do not include passwords, authentication tokens, confidential research data, or other sensitive information in support requests.

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check .
```

## About

**ARKEO** is a modular photovoltaic and optoelectronic characterization platform developed by **CICCI Research**.

https://www.cicciresearch.com/

## License

Copyright © CICCI Research s.r.l.

All rights reserved. No permission is granted to copy, modify, redistribute, or commercially use this software without prior written authorization from CICCI Research s.r.l.
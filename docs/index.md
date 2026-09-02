# ARKEO NOMAD Plugin

The **ARKEO NOMAD Plugin** connects CICCI Research ARKEO measurement data with **NOMAD Oasis**.

It allows supported ARKEO TXT files to be uploaded directly to NOMAD and converted into structured, searchable research data.

## What it does

- Recognizes supported ARKEO measurement files
- Parses ARKEO Stability data automatically
- Creates structured NOMAD entries
- Adds ARKEO-specific metadata and results
- Provides a dedicated **ARKEO Explorer**

## Current support

Version **0.1.0** supports ARKEO Stability measurements composed of:

- Stability (Parameters)
- Stability (Tracking)
- Stability (JV)

No manually created `.archive.yaml` file is required for supported ARKEO measurements.

## Stable release

The current stable release is **v0.1.0**.

For production or institutional installations, use the tagged release rather than the development version on `main`.

## Documentation

- [Installation](how_to/install_this_plugin.md)
- [How to use](how_to/use_this_plugin.md)
- [Support](support.md)
- [Release v0.1.0](https://github.com/cicciresearch/nomad-arkeo-plugin/releases/tag/v0.1.0)
- [GitHub repository](https://github.com/cicciresearch/nomad-arkeo-plugin)

## About

**ARKEO** is a modular photovoltaic and optoelectronic characterization platform developed by **CICCI Research s.r.l**.

The ARKEO NOMAD Plugin is an independent integration developed and maintained by CICCI Research for use with NOMAD Oasis.

**NOMAD** is developed by the NOMAD/FAIRmat community. This documentation does not imply endorsement, certification, or official partnership by NOMAD or FAIRmat.

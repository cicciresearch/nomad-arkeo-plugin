# nomad-arkeo-plugin

Prototype NOMAD plugin for **CICCI Research ARKEO** photovoltaic measurement data.

This first version follows the same overall NOMAD architecture used by Quantum
Yield Berlin's `nomad-luqy-plugin`:

- a **parser** for the instrument raw text files;
- a **Python schema package**;
- a dedicated **ARKEO Explorer** NOMAD app;
- an **example upload**.

## v0.1.0 scope

The first implementation supports an ARKEO **Stability** export consisting of:

- `Stability (Parameters)` — NOMAD mainfile;
- `Stability (Tracking)` — MPPT time series;
- `Stability (JV)` — JV snapshot.

The parser creates one `ArkeoStabilityMeasurement` from the Parameters file and
looks in the same directory for the corresponding Tracking and JV files.

The schema includes instrument provenance, sample/cell settings, irradiance, JV
settings, stability/MPPT settings, tracking arrays, forward/reverse JV arrays and
parameters, stability summary arrays, and source filenames.

## ARKEO provenance

Legacy ARKEO files do not contain a formal instrument block. v0.1.0 identifies
them using both the filename convention and characteristic ARKEO header sections.
The structured entry records that this identity was inferred.

Future ARKEO exports should add:

```text
[Instrument]
Manufacturer	CICCI Research
Product	ARKEO
Model	ARKEO Multichannel
Serial Number	ARK-2026-00123
Software	ARKEO Control
Software Version	...
Data Format	CICCI-ARKEO-1
```

The parser already reads these fields when they are present.

## ARKEO Explorer

The plugin registers **ARKEO Explorer**, locked to the ARKEO schema. It provides
search/filter fields for instrument, model, device, date, irradiance, tracking
algorithm, duration, Voc, Jsc, fill factor and efficiency.

This is the intended mechanism for finding ARKEO measurements. A global CICCI
Dataset is not required simply to make entries discoverable.

## Development

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
pytest -q
```

Target NOMAD version: **1.4.3**.

## Oasis installation

The plugin must be installed in the Python environment used by the NOMAD Oasis
`app` and `worker`; uploading this repository as raw data is not enough.

For a standard NOMAD distribution, host the plugin in Git and add it to the
distribution's plugin dependencies, e.g.:

```toml
[project.optional-dependencies]
plugins = [
  "nomad-arkeo-plugin @ git+https://github.com/<CICCI-ORG>/nomad-arkeo-plugin.git@<COMMIT>"
]
```

Then build/use the resulting custom distribution image and restart the Oasis.

## Not implemented yet

- standalone JV-only uploads;
- EIS / IMPS / IMVS / TPV / TPC / EQE and other ARKEO routines;
- automatic Central NOMAD upload;
- DOI/dataset creation;
- website synchronization;
- notifications to CICCI.

## License

To be selected by CICCI Research before public release.

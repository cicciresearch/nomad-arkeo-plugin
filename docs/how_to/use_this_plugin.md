# Using the ARKEO NOMAD Plugin

## 1. Open NOMAD Oasis

Open your institution's NOMAD Oasis installation and sign in.

## 2. Create an upload

Go to:

```text
PUBLISH → Uploads
```

Create a new upload.

## 3. Upload ARKEO files

Upload the original ARKEO TXT files belonging to the same measurement.

For an ARKEO Stability measurement, this normally includes:

```text
Stability (Parameters)
Stability (Tracking)
Stability (JV)
```

Keep the files together in the same folder.

No manually created `.archive.yaml` file is required for supported ARKEO measurements.

## 4. Wait for processing

NOMAD automatically recognizes the ARKEO Stability Parameters file.

The plugin then looks for the associated Tracking and JV files and creates one structured ARKEO measurement entry.

## 5. Open the structured entry

Open the generated entry to inspect the parsed measurement information, including:

- device and cell settings;
- channel settings;
- irradiance;
- JV settings and results;
- stability and MPPT settings;
- tracking data;
- source filenames.

## 6. Explore ARKEO measurements

Go to:

```text
EXPLORE → ARKEO
```

Use the available filters to search and compare structured ARKEO measurements.

## Privacy

Uploading ARKEO data does not automatically publish it.

Privacy, sharing, and publication are controlled by the NOMAD Oasis installation and by the data owner.

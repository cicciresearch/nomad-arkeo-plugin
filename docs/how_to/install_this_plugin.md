# Install the CICCI Research ARKEO Plugin

The ARKEO plugin lets a **NOMAD Oasis** recognize original CICCI Research ARKEO `.txt` files and convert them automatically into structured NOMAD entries.

> This guide assumes that NOMAD Oasis is already installed and working.  
> If not, install it first using the official NOMAD guide:  
> https://docs.nomad-lab.eu/1.4.3/howto/oasis/install.html

## 1. Place the plugin next to your NOMAD Oasis

Example:

```text
C:\NOMAD\
├── nomad-oasis\
└── nomad-arkeo-plugin\
```

## 2. Create the ARKEO NOMAD image

From the NOMAD Oasis folder, check the image in use:

```bash
docker inspect nomad_oasis_app --format "{{.Config.Image}}"
```

For a standard installation:

```bash
docker tag ghcr.io/fairmat-nfdi/nomad-distro-template:main nomad-oasis-base:current
```

In the parent folder create `Dockerfile.arkeo`:

```dockerfile
FROM ghcr.io/astral-sh/uv:0.7 AS uv
FROM nomad-oasis-base:current

USER root
COPY --from=uv /uv /usr/local/bin/uv
COPY nomad-arkeo-plugin /tmp/nomad-arkeo-plugin
RUN uv pip install --python /opt/venv/bin/python --no-deps /tmp/nomad-arkeo-plugin && rm -rf /tmp/nomad-arkeo-plugin
USER nomad
```

Build it:

```bash
docker build -f Dockerfile.arkeo -t nomad-oasis-arkeo:0.1.0 .
```

## 3. Tell NOMAD to use the ARKEO image

Inside `nomad-oasis`, create `docker-compose.arkeo.yml`:

```yaml
services:
  app:
    image: nomad-oasis-arkeo:0.1.0

  worker:
    image: nomad-oasis-arkeo:0.1.0
```

Then run:

```bash
docker compose -f docker-compose.yaml -f docker-compose.arkeo.yml up -d --force-recreate app worker
```

If you see `502 Bad Gateway`:

```bash
docker compose -f docker-compose.yaml -f docker-compose.arkeo.yml restart proxy
```

## 4. Check that ARKEO is active

Open NOMAD and go to:

```text
EXPLORE → ARKEO
```

If **Explore ARKEO** appears, the plugin is installed.

## 5. Upload ARKEO data

Create a new NOMAD upload and upload the original ARKEO files in the same folder, for example:

```text
..._Stability (Parameters)_Sample-1A.txt
..._Stability (Tracking)_Sample-1A.txt
..._Stability (JV)_Sample-1A.txt
```

No `.archive.yaml` file is needed.

The plugin automatically creates a structured ARKEO entry.

## 6. Explore the results

Go to:

```text
EXPLORE → ARKEO
```

You can search/filter by Manufacturer, Instrument, Device, Tracking algorithm, Irradiance, Voc, Jsc, Fill factor, Efficiency, and other parsed values.

Private NOMAD data remain private unless the university explicitly shares or publishes them.

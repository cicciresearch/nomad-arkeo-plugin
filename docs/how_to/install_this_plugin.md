# Install the ARKEO NOMAD Plugin

The ARKEO NOMAD Plugin allows a **NOMAD Oasis** installation to recognize supported CICCI Research ARKEO `.txt` measurement files and convert them into structured NOMAD entries.

> This guide assumes that NOMAD Oasis is already installed and working.
>
> Current plugin target: **NOMAD 1.4.3**

## 1. Clone the plugin

Place the plugin next to your NOMAD Oasis installation.

Example:

```text
C:\NOMAD\
├── nomad-oasis\
└── nomad-arkeo-plugin\
```

Clone the repository:

```bash
cd C:\NOMAD
git clone --branch v0.1.0 --depth 1 https://github.com/cicciresearch/nomad-arkeo-plugin.git
```

## 2. Build the ARKEO-enabled NOMAD image

First check which image your NOMAD Oasis `app` container is using:

```bash
docker inspect nomad_oasis_app --format "{{.Config.Image}}"
```

For a standard NOMAD distribution, create a local base tag:

```bash
docker tag ghcr.io/fairmat-nfdi/nomad-distro-template:main nomad-oasis-base:current
```

In `C:\NOMAD`, create a file named:

```text
Dockerfile.arkeo
```

with:

```dockerfile
FROM ghcr.io/astral-sh/uv:0.7 AS uv
FROM nomad-oasis-base:current

USER root
COPY --from=uv /uv /usr/local/bin/uv
COPY nomad-arkeo-plugin /tmp/nomad-arkeo-plugin

RUN uv pip install --python /opt/venv/bin/python --no-deps /tmp/nomad-arkeo-plugin \
    && rm -rf /tmp/nomad-arkeo-plugin

USER nomad
```

Build the image:

```bash
docker build -f Dockerfile.arkeo -t nomad-oasis-arkeo:0.1.0 .
```

## 3. Enable the plugin in NOMAD Oasis

Inside the `nomad-oasis` folder, create:

```text
docker-compose.arkeo.yml
```

with:

```yaml
services:
  app:
    image: nomad-oasis-arkeo:0.1.0

  worker:
    image: nomad-oasis-arkeo:0.1.0
```

Start the ARKEO-enabled `app` and `worker`:

```bash
docker compose -f docker-compose.yaml -f docker-compose.arkeo.yml up -d --force-recreate app worker
```

## 4. Verify the installation

Open your NOMAD Oasis in the browser.

Go to:

```text
EXPLORE → ARKEO
```

If **ARKEO** appears in the Explore menu, the plugin is active.

## 5. Upload ARKEO data

Create a new NOMAD upload and add the original ARKEO files belonging to the same measurement.

For a Stability measurement, this normally includes:

```text
..._Stability (Parameters)_Demo-Cell-01.txt
..._Stability (Tracking)_Demo-Cell-01.txt
..._Stability (JV)_Demo-Cell-01.txt
```

Keep the files together in the same folder.

No manually created `.archive.yaml` file is required for supported ARKEO measurements.

The plugin automatically creates the structured ARKEO entry.

## Troubleshooting

### 502 Bad Gateway

If NOMAD returns `502 Bad Gateway` after recreating the containers:

```bash
docker compose -f docker-compose.yaml -f docker-compose.arkeo.yml restart proxy
```

Then reload NOMAD in the browser.

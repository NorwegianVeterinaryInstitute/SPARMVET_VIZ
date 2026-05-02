# SPARMVET-VIZ — Production Container
#
# Includes:
#   - Python 3.12 + all app dependencies
#   - Quarto (for report rendering: HTML, PDF, DOCX)
#   - LuaLaTeX via texlive-luatex (for PDF output)
#   - Pandoc (bundled with Quarto)
#
# Build:
#   docker build -t sparmvet-viz:latest -f assets/containers/Dockerfile .
#
# Run (filesystem connector, developer persona):
#   docker run --rm -p 8001:8001 \
#     -v /data/my_project:/data \
#     -e SPARMVET_PROFILE=/data/profile.yaml \
#     sparmvet-viz:latest
#
# Run (pipeline mode, static persona, data injected via volume):
#   docker run --rm -p 8001:8001 \
#     -v /pipeline/output:/pipeline/output:ro \
#     -v /pipeline/config:/app/config/deployment/pipeline:ro \
#     -e SPARMVET_PROFILE=/app/config/deployment/pipeline/profile.yaml \
#     -e SPARMVET_PERSONA=/app/config/deployment/pipeline/persona.yaml \
#     sparmvet-viz:latest

FROM python:3.12-slim

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    # LaTeX for Quarto PDF rendering
    texlive-luatex \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-plain-generic \
    texlive-latex-extra \
    lmodern \
    # libGL for plotnine/matplotlib SVG/PDF backends
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ── Quarto ────────────────────────────────────────────────────────────────────
# Pin version for reproducibility; update as needed.
ARG QUARTO_VERSION=1.8.27
RUN wget -qO /tmp/quarto.deb \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb" \
    && dpkg -i /tmp/quarto.deb \
    && rm /tmp/quarto.deb

# ── App ───────────────────────────────────────────────────────────────────────
WORKDIR /app

# Install Python dependencies before copying code (layer cache)
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        polars \
        shiny \
        numpy \
        pandas \
        pyyaml \
        plotnine \
        fastexcel \
        requests \
        jinja2 \
        pyarrow

# Copy application code
COPY app/         app/
COPY libs/        libs/
COPY config/      config/
COPY connector/   connector/
COPY ingestion/   ingestion/
COPY utils/       utils/

# Install local libraries (editable installs not needed in prod)
RUN pip install --no-cache-dir \
    libs/viz_factory \
    libs/viz_gallery \
    libs/transformer \
    libs/ingestion \
    libs/generator_utils \
    libs/utils \
    libs/connector \
    2>/dev/null || true

# ── Runtime ───────────────────────────────────────────────────────────────────
ENV PYTHONPATH=/app
EXPOSE 8001

CMD ["python", "-m", "shiny", "run", "app/src/main.py", \
     "--host", "0.0.0.0", "--port", "8001"]

# ============================================================================
# Testlane.ai Sovereign AI — Production Dockerfile
# Google Cloud Run (python:3.12-slim, non-root, WhiteNoise, Gunicorn)
# ============================================================================
FROM python:3.12-slim

# --- Build-time metadata ---
LABEL org.opencontainers.image.source="https://github.com/nous/testlane-project"
LABEL org.opencontainers.image.description="Testlane.ai Sovereign AI Platform — Cloud Run container"

# --- System dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --- Non-root user ---
RUN groupadd --system testlane && \
    useradd --system --gid testlane --no-create-home --home-dir /app testlane

WORKDIR /app

# --- Python dependencies (cached layer) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Application code ---
COPY . .

# --- Static files (built into the image — no runtime collectstatic) ---
RUN python manage.py collectstatic --noinput --clear

# --- Ownership (non-root runtime) ---
RUN chown -R testlane:testlane /app

# --- Drop privileges ---
USER testlane

# --- Runtime config ---
ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=semilattice_project.settings

EXPOSE 8080

# Gunicorn: workers=2, threads=4 (optimised for Cloud Run 1 vCPU / 512 MiB)
CMD exec gunicorn semilattice_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --worker-tmp-dir /dev/shm
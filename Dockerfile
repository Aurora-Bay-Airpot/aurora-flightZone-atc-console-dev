# ── FlightZone ATC Chatbot ──────────────────────────────────────────────────────
# Build:  docker build -t flightzone .
# Run:    docker run --env-file .env -p 8000:8000 flightzone
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.11-slim

# ── System setup ──────────────────────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY this.py .

# ── Security: run as non-root ─────────────────────────────────────────────────
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# ── Runtime ──────────────────────────────────────────────────────────────────
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "this:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]

FROM python:3.13-slim

# Prevent Python from writing .pyc files & enable real-time logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for health checks & uv for ultra-fast dependency installation
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Layer Caching: Install dependencies first so code changes rebuild in seconds
COPY pyproject.toml .
RUN uv pip install --system .

# Copy application source code
COPY . .
RUN chmod +x entrypoint.sh

# Expose Streamlit frontend (8501) and FastAPI backend (8000)
EXPOSE 8501 8000

CMD ["./entrypoint.sh"]

# Use a lightweight official Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (curl is needed for uv installation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager for extremely fast installs
RUN pip install --no-cache-dir uv

# Copy the project files to the container
COPY . /app

# Install the Python dependencies directly to the system python environment
RUN uv pip install --system -r requirements.txt

# Expose the port used by Streamlit (8501) and FastAPI (8000)
EXPOSE 8501
EXPOSE 8000

# Start the Streamlit application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]

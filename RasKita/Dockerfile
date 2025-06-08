# Base image: Python 3.11 slim
FROM python:3.11-slim

# Install only essential system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies (no venv, global install)
COPY Backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend source
COPY Backend /app/Backend
COPY Frontend /app/Frontend

# Move to backend folder
WORKDIR /app/Backend

# Expose required port
EXPOSE 7860

# Start the app using uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

# Use Python 3.10 slim as the base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY process.py .

# Set default environment variable
ENV APP_NAME="Data Engineer"

# Run the application
CMD ["python", "process.py"]

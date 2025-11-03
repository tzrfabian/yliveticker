# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY setup.py .
COPY README.md .

# Copy the application code
COPY yliveticker/ ./yliveticker/

# Install the package and its dependencies
RUN pip install --no-cache-dir -e .

# Set environment variable for protobuf compatibility
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Default command runs the client code
CMD ["python", "-u", "yliveticker/client_code.py"]


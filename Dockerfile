# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY setup.py .
COPY README.md .

# Copy the application code
COPY yliveticker/ ./yliveticker/
COPY server.py ./server.py

# Install the package and its dependencies
RUN pip install --no-cache-dir -e .

# Set environment variable for protobuf compatibility
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Expose the websocket server port
EXPOSE 8000

# Default command runs the websocket server
CMD ["python", "-u", "server.py"]


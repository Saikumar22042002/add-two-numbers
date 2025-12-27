# Stage 1: Build stage with dependencies
FROM python:3.11-slim as builder

WORKDIR /opt/app

# Create a non-privileged user for security
RUN useradd --create-home --shell /bin/bash appuser

# Create and activate a virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies into the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final production image
FROM python:3.11-slim

WORKDIR /opt/app

# Create the same non-privileged user
RUN useradd --create-home --shell /bin/bash appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY app.py .

# Set environment to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Ensure the app user owns the files
RUN chown -R appuser:appuser /opt/app

# Switch to the non-privileged user
USER appuser

# Expose the application port
EXPOSE 5000

# Command to run the application using Gunicorn
# Using 2 workers as a sensible default for a small service
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]

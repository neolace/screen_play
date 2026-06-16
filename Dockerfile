FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Install fonts for annotations
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY config.py .
COPY annotations.py .
COPY engine.py .
COPY run_test.py .
COPY example_steps.py .

# Default output directory (mount a volume here to retrieve screenshots)
RUN mkdir -p /app/reports
VOLUME ["/app/reports"]

# Default: run the example steps
ENTRYPOINT ["python", "run_test.py"]
CMD ["--steps", "example_steps.py"]

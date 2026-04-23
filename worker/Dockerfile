# Build stage
FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Run stage
FROM python:3.12-alpine

WORKDIR /app

# Copy installed dependencies
COPY --from=builder /install /usr/local

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY . .

# Minimal python script checking redis connectivity for healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import os, redis; r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=int(os.getenv('REDIS_PORT', 6379)), password=os.getenv('REDIS_PASSWORD', None)); r.ping()" || exit 1

CMD ["python", "-u", "worker.py"]

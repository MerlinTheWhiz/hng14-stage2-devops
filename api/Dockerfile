# Build stage
FROM python:3.11-alpine AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Run stage
FROM python:3.11-alpine

WORKDIR /app

# Install curl for healthcheck
# hadolint ignore=DL3018
RUN apk add --no-cache curl

# Copy installed dependencies
COPY --from=builder /install /usr/local

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

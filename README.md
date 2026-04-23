# DevOps Stage 2 — Containerized Microservices Job System

## Overview

This project is a containerized microservices system consisting of:

- **Frontend (Node.js)** — UI for submitting and tracking jobs
- **API (FastAPI Python)** — Job creation and status management
- **Worker (Python)** — Background job processor
- **Redis** — Shared in-memory queue and datastore

The system is fully containerized using Docker and Docker Compose. A CI/CD pipeline using GitHub Actions handles linting, testing, building, scanning, integration testing, and deployment simulation.

---

## Prerequisites

Ensure the following are installed on your machine:

- Docker ≥ 24
- Docker Compose v2+
- Git
- Python 3.11 (optional for local testing)
- Node.js 18+ (optional for frontend debugging)

---

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-fork-url>
cd hng14-stage2-devops
```

### 2. Configure Environment

```bash
cp .env.example .env
```

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=yourpassword
QUEUE_NAME=job
PORT=3000
API_URL=http://api:8000


### 3. Start the Stack

```bash
docker compose up -d --build
```

### 4. Verify the Application

Navigate to `http://localhost:3000` in your browser.

### 5. Stop the Stack

```bash
docker compose down -v
```

---

## API Endpoints

Create Job
POST /jobs

Response:

{
  "job_id": "uuid"
}


Get Job Status
GET /jobs/{job_id}

Response:

{
  "job_id": "uuid",
  "status": "queued | processing | completed | failed"
}


Health Check
GET /health

Response:

{
  "status": "healthy"
}


Running Tests

Run unit tests:

pytest api/tests/

All Redis interactions are mocked using unittest.mock, ensuring no external dependency during tests.

---

## CI/CD Pipeline

The GitHub Actions pipeline runs automatically on every push and pull request to the `main` branch.

### Pipeline Stages

1. **Linting** — Checks for Python and Dockerfile style issues
2. **Testing** — Runs unit tests with coverage
3. **Build & Push** — Builds Docker images and pushes them to a local registry
4. **Security Scan** — Scans images for vulnerabilities using Trivy
5. **Integration Test** — Runs end-to-end tests using Docker Compose
6. **Deploy** — Simulates a rolling update deployment

---

## Fixes and Improvements

See [FIXES.md](FIXES.md) for detailed information about bug fixes and architectural improvements.

---

## Successful Startup Checklist

When working correctly:

Containers must be healthy:
api
worker
frontend
redis

Worker logs show:
Processing job <id>
Done: <id>

API responds:
/jobs
/jobs/{id}
/health
Frontend:
Can submit jobs
Can track job status live

---
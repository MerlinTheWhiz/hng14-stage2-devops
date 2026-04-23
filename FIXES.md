## API - main.py

- File: api/main.py  
  Line: Redis client initialization  
  Problem: Redis connection was hardcoded to "localhost:6379"  
  Why this is a problem: In containerized environments, "localhost" refers to the container itself, not the Redis service, causing connection failure in production  
  Fix: Replaced hardcoded Redis configuration with environment variables (REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

- File: api/main.py  
  Line: configuration section  
  Problem: Queue name was hardcoded as "job"  
  Why this is a problem: Hardcoded values reduce flexibility and prevent multi-environment deployment  
  Fix: Moved queue name to environment variable QUEUE_NAME with default fallback

- File: api/main.py  
  Line: get_job endpoint  
  Problem: Returned {"error": "not found"} with HTTP 200 status  
  Why this is a problem: REST APIs must use proper HTTP status codes for error handling; returning 200 breaks client-side logic and monitoring  
  Fix: Replaced with HTTPException(404)

- File: api/main.py  
  Line: exception handling  
  Problem: No handling for Redis connection failures  
  Why this is a problem: Redis downtime would crash or silently break the API  
  Fix: Added try/except redis.ConnectionError with HTTP 500 response

- File: api/main.py  
  Line: missing endpoint  
  Problem: No health check endpoint existed  
  Why this is a problem: Docker health checks and CI/CD pipelines require a reliable endpoint to verify service readiness  
  Fix: Added /health endpoint returning service status



  ## Frontend - index.html

- File: frontend/views/index.html  
  Line: submitJob function  
  Problem: No handling of failed HTTP responses from the API  
  Why this is a problem: The frontend assumed all API responses were successful (HTTP 200), which breaks when the API returns 4xx or 5xx errors  
  Fix: Added res.ok check and displayed API error messages when requests fail

- File: frontend/views/index.html  
  Line: submitJob function  
  Problem: No handling of network failures  
  Why this is a problem: If the backend is unreachable, the UI would silently fail without feedback  
  Fix: Added try/catch block with user-visible error message

- File: frontend/views/index.html  
  Line: pollJob function  
  Problem: Polling logic did not properly handle API error responses  
  Why this is a problem: Could cause infinite polling loops or undefined state handling when backend fails  
  Fix: Added res.ok validation and early return on error responses

- File: frontend/views/index.html  
  Line: pollJob function  
  Problem: No defensive checks on status value  
  Why this is a problem: Undefined or malformed API responses could break polling logic  
  Fix: Added validation check (data.status exists before comparison)

- File: frontend/views/index.html  
  Line: error handling  
  Problem: Backend error messages were not surfaced to the user  
  Why this is a problem: Hides debugging information and reduces observability  
  Fix: Displayed server-provided error messages with fallback to 'Unknown error'


## Frontend - app.js

- File: frontend/app.js  
  Line: API_URL declaration  
  Problem: API endpoint was hardcoded to "http://localhost:8000"  
  Why this is a problem: Hardcoded service URLs break in containerized or distributed environments where services communicate via service names rather than localhost  
  Fix: Moved API URL to environment variable (API_URL) with fallback for local development

- File: frontend/app.js  
  Line: PORT configuration  
  Problem: Server port was hardcoded to 3000  
  Why this is a problem: Cloud and container environments often require dynamic port assignment  
  Fix: Replaced with environment variable PORT with fallback value

- File: frontend/app.js  
  Line: error handling in /submit route  
  Problem: All API errors were mapped to generic HTTP 500 response  
  Why this is a problem: It hides real backend error types (e.g., 404, 400, 503), making debugging and integration testing unreliable  
  Fix: Forwarded actual HTTP status codes from backend responses

- File: frontend/app.js  
  Line: error message extraction  
  Problem: Error messages were not properly extracted from API responses  
  Why this is a problem: Users and integration tests receive uninformative error messages  
  Fix: Extracted detailed error messages using optional chaining (err.response?.data?.detail)

- File: frontend/app.js  
  Line: logging  
  Problem: Server startup logs did not reflect runtime configuration  
  Why this is a problem: Makes debugging in containerized environments difficult  
  Fix: Updated logs to include dynamic PORT value


## Worker - worker.py

- File: worker/worker.py  
  Line: imports / configuration section  
  Problem: Redis host, port, password, and queue name were hardcoded  
  Why this is a problem: Breaks containerized deployment where services communicate via Docker DNS and environment-based config  
  Fix: Replaced hardcoded values with environment variables (REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, QUEUE_NAME)

- File: worker/worker.py  
  Line: 6–7  
  Problem: No configurable queue name  
  Why this is a problem: Makes the system rigid and not environment-agnostic  
  Fix: Introduced QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

- File: worker/worker.py  
  Line: signal handling section  
  Problem: Worker had no graceful shutdown mechanism  
  Why this is a problem: Containers may terminate mid-job, causing lost or inconsistent job states  
  Fix: Added SIGTERM and SIGINT handlers to safely stop the worker loop

- File: worker/worker.py  
  Line: process_job() function  
  Problem: No job state tracking or failure handling  
  Why this is a problem: Failures were silent and jobs could remain stuck in "queued" forever  
  Fix: Added status transitions (processing → completed) and exception handling that marks jobs as failed

- File: worker/worker.py  
  Line: main loop (brpop usage)  
  Problem: Worker used blocking Redis call without runtime resilience  
  Why this is a problem: Redis downtime would cause undefined behavior or silent failure  
  Fix: Wrapped loop in running flag and added Redis connection error handling with retry delay

- File: worker/worker.py  
  Line: brpop("job", timeout=5)  
  Problem: Queue name was hardcoded  
  Why this is a problem: Prevents environment-based configuration and breaks multi-environment deployments  
  Fix: Replaced "job" with QUEUE_NAME environment variable

- File: worker/worker.py  
  Line: exception handling  
  Problem: No fallback behavior on runtime failure  
  Why this is a problem: Worker would crash instead of recovering from temporary Redis outages  
  Fix: Added exception handling for Redis.ConnectionError with retry delay
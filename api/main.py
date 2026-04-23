from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush(QUEUE_NAME, job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Redis connection failed")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    try:
        status = r.hget(f"job:{job_id}", "status")
        if not status:
            raise HTTPException(status_code=404, detail="not found")
        return {"job_id": job_id, "status": status.decode()}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Redis connection failed")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
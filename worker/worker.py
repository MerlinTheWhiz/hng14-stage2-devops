import redis
import time
import os
import signal

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
running = True

def handle_shutdown(signum, frame):
    global running
    print("Received shutdown signal. Gracefully exiting...")
    running = False

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def process_job(job_id):
    print(f"Processing job {job_id}")
    try:
        r.hset(f"job:{job_id}", "status", "processing")
        time.sleep(2)
        r.hset(f"job:{job_id}", "status", "completed")
        print(f"Done: {job_id}")
    except Exception as e:
        r.hset(f"job:{job_id}", "status", "failed")
        print(f"Failed job {job_id}: {e}")

while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode())
    except redis.ConnectionError:
        print("Waiting for Redis...")
        time.sleep(5)
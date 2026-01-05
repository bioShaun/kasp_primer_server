# Result Cleanup Design (Phase 6)

## Objective
Implement automatic cleanup of old job directories to prevent disk exhaustion.

## Strategy
Use a native `asyncio` background task within FastAPI. No external dependencies.

## Configuration (`config.py`)
Add environment-variable-backed settings:
```python
RETENTION_HOURS = int(os.getenv("RETENTION_HOURS", "24"))
CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL", "3600"))  # 1 hour
```

## Implementation

### Cleanup Function (`main.py`)
```python
import asyncio
import shutil
import time
import logging

logger = logging.getLogger("uvicorn.error")

async def cleanup_old_jobs():
    """Background task to clean up old job directories."""
    while True:
        try:
            now = time.time()
            cutoff = now - (RETENTION_HOURS * 3600)
            for job_dir in WORK_DIR.iterdir():
                if job_dir.is_dir() and job_dir.stat().st_mtime < cutoff:
                    logger.info(f"Cleaning up old job: {job_dir.name}")
                    shutil.rmtree(job_dir, ignore_errors=True)
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
```

### Lifecycle Events
```python
@app.on_event("startup")
async def start_cleanup_task():
    asyncio.create_task(cleanup_old_jobs())
```

## Error Handling
- `shutil.rmtree(..., ignore_errors=True)` prevents crashes on permission issues.
- Outer `try/except` logs errors without stopping the loop.

## Testing
Set `RETENTION_HOURS=0` and `CLEANUP_INTERVAL=60` temporarily to verify old jobs are deleted.

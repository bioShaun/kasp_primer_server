# AI Executable Task: Implement Result Cleanup (Phase 6)

## Context
Implement automatic cleanup of old job directories in the KASP Primer Design backend.

## Files to Modify
- `backend/config.py`
- `backend/main.py`

---

## Step 1: Update `config.py`

Add the following lines after `MAX_SNP_COUNT`:

```python
# Cleanup settings
RETENTION_HOURS = int(os.getenv("RETENTION_HOURS", "24"))
CLEANUP_INTERVAL_SECONDS = int(os.getenv("CLEANUP_INTERVAL", "3600"))
```

---

## Step 2: Update `main.py`

### 2.1 Add imports at the top

Add these imports if not present:
```python
import asyncio
import shutil
import time
import logging
```

### 2.2 Add logger after imports

```python
logger = logging.getLogger("uvicorn.error")
```

### 2.3 Update config import

Change the config import to include new settings:
```python
from config import GENOMES_CONFIG, WORK_DIR, MAX_SNP_COUNT, RETENTION_HOURS, CLEANUP_INTERVAL_SECONDS
```

### 2.4 Add cleanup function before `@app.get("/api/genomes")`

```python
async def cleanup_old_jobs():
    """Background task to clean up old job directories."""
    while True:
        try:
            now = time.time()
            cutoff = now - (RETENTION_HOURS * 3600)
            if WORK_DIR.exists():
                for job_dir in WORK_DIR.iterdir():
                    if job_dir.is_dir():
                        try:
                            mtime = job_dir.stat().st_mtime
                            if mtime < cutoff:
                                logger.info(f"Cleaning up old job: {job_dir.name}")
                                shutil.rmtree(job_dir, ignore_errors=True)
                        except OSError:
                            pass
        except Exception as e:
            logger.error(f"Cleanup task error: {e}")
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)


@app.on_event("startup")
async def start_cleanup_task():
    """Start the background cleanup task."""
    asyncio.create_task(cleanup_old_jobs())
```

---

## Step 3: Verify

1. Restart the backend server.
2. Check logs for "Cleaning up old job" messages (if old jobs exist).
3. Optionally test with `RETENTION_HOURS=0` to trigger immediate cleanup.

---

## Expected Result
Old job directories in `/tmp/kasp_jobs/` are automatically deleted after 24 hours.

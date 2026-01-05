from pathlib import Path
import os
import yaml

BASE_DIR = Path(__file__).parent

# Config file paths
SYSTEM_CONFIG = Path(os.getenv("SYSTEM_CONFIG", BASE_DIR / "config.yaml"))
GENOMES_CONFIG = Path(os.getenv("GENOME_CONFIG", BASE_DIR / "genomes.yaml"))

# Work directory
WORK_DIR = Path(os.getenv("WORK_DIR", BASE_DIR / "jobs"))

# Load system settings from YAML
with open(SYSTEM_CONFIG) as f:
    _sys_config = yaml.safe_load(f)

# Cleanup settings
_cleanup = _sys_config.get("cleanup", {})
RETENTION_HOURS = _cleanup.get("retention_hours", 24)
CLEANUP_INTERVAL_SECONDS = _cleanup.get("interval_seconds", 3600)

# Limits
_limits = _sys_config.get("limits", {})
MAX_SNP_COUNT = _limits.get("max_snp_count", 50)

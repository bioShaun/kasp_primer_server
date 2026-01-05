from pathlib import Path
import os

BASE_DIR = Path(__file__).parent
GENOMES_CONFIG = Path(os.getenv("GENOME_CONFIG", BASE_DIR / "genomes.yaml"))
WORK_DIR = Path(os.getenv("WORK_DIR", "/tmp/kasp_jobs"))
MAX_SNP_COUNT = 50  # MVP 限制

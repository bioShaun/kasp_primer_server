import uuid
import subprocess
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yaml

from config import GENOMES_CONFIG, WORK_DIR, MAX_SNP_COUNT

app = FastAPI(title="KASP Primer Design API")

# 挂载静态文件
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError:
    # Static directory doesn't exist yet (development mode)
    pass


class DesignRequest(BaseModel):
    snps: str
    genome: str


@app.get("/api/genomes")
def get_genomes():
    """返回可用基因组列表"""
    with open(GENOMES_CONFIG) as f:
        config = yaml.safe_load(f)
    return config.get("genomes", [])


@app.post("/api/design")
def submit_design(req: DesignRequest):
    """提交设计任务"""
    # 验证 SNP 数量
    lines = [l for l in req.snps.strip().split("\n") if l.strip()]
    if len(lines) > MAX_SNP_COUNT:
        raise HTTPException(400, f"最多支持 {MAX_SNP_COUNT} 个 SNP")
    
    # 获取基因组路径
    with open(GENOMES_CONFIG) as f:
        config = yaml.safe_load(f)
    
    genome_info = None
    for genome in config.get("genomes", []):
        if genome["id"] == req.genome:
            genome_info = genome
            break
    
    if not genome_info:
        raise HTTPException(400, f"基因组 {req.genome} 不存在")
    
    genome_path = genome_info["path"]
    
    # 创建任务目录
    job_id = str(uuid.uuid4())
    job_dir = WORK_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入输入文件
    input_file = job_dir / "input.txt"
    input_file.write_text(req.snps)
    
    # 执行 Pipeline （使用位置参数）
    try:
        result = subprocess.run(
            ["snp-primer", str(input_file), genome_path, "-o", str(job_dir)],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode != 0:
            (job_dir / "error.log").write_text(result.stderr)
            return {"job_id": job_id, "status": "failed", "error": result.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"job_id": job_id, "status": "timeout"}
    except FileNotFoundError:
        # snp-primer not found - return helpful error
        return {
            "job_id": job_id, 
            "status": "failed", 
            "error": "snp-primer command not found. Please install SNP_Primer_Pipeline3."
        }
    
    return {"job_id": job_id, "status": "completed"}


@app.get("/api/job/{job_id}")
def get_job(job_id: str):
    """获取任务结果"""
    job_dir = WORK_DIR / job_id
    if not job_dir.exists():
        raise HTTPException(404, "任务不存在")
    
    # 检查错误
    error_file = job_dir / "error.log"
    if error_file.exists():
        return {"status": "failed", "error": error_file.read_text()}
    
    # 解析结果 - 使用 summary 文件
    result_file = job_dir / "all_KASP_primers_summary.txt"
    if not result_file.exists():
        return {"status": "pending"}
    
    # 解析 TSV 为 JSON
    results = []
    with open(result_file) as f:
        headers = f.readline().strip().split("\t")
        for line in f:
            values = line.strip().split("\t")
            results.append(dict(zip(headers, values)))
    
    return {"status": "completed", "results": results}


@app.get("/api/download/{job_id}/{filename}")
def download_file(job_id: str, filename: str):
    """下载结果文件"""
    allowed = ["all_KASP_primers.txt", "all_KASP_primers_summary.txt"]
    if filename not in allowed:
        raise HTTPException(400, "不允许下载此文件")
    
    file_path = WORK_DIR / job_id / filename
    if not file_path.exists():
        raise HTTPException(404, "文件不存在")
    
    return FileResponse(file_path, filename=filename)


@app.get("/")
def root():
    """返回前端主页"""
    try:
        return FileResponse("static/index.html")
    except Exception:
        return {"message": "KASP Primer Design API", "docs": "/docs"}

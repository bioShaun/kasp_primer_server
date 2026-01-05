# Stage 1: Build Frontend
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Runtime
FROM --platform=linux/amd64 python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ncbi-blast+ git && rm -rf /var/lib/apt/lists/*

# Add pipeline binaries to PATH
ENV PATH="/usr/local/lib/python3.10/site-packages/snp_primer_pipeline/bin:${PATH}"

# Muscle source compilation removed due to build errors. 
# Pipeline handles muscle failure gracefully.

RUN pip install --no-cache-dir \
    git+https://github.com/bioShaun/SNP_Primer_Pipeline3.git \
    fastapi uvicorn[standard] pyyaml python-multipart

COPY --from=frontend /app/dist /app/static
COPY backend/ /app
# Use Docker-specific genome configuration
COPY backend/genomes.docker.yaml /app/genomes.yaml
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

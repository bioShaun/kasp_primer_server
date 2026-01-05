# Stage 1: Build Frontend
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Runtime
FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ncbi-blast+ git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    git+https://github.com/bioShaun/SNP_Primer_Pipeline3.git \
    fastapi uvicorn[standard] pyyaml python-multipart

COPY --from=frontend /app/dist /app/static
COPY backend/ /app
WORKDIR /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

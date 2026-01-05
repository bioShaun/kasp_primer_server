# KASP Primer Design Service

基于 `SNP_Primer_Pipeline3` 构建的 KASP 引物设计 Web 服务。

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus
- **后端**: FastAPI + Uvicorn
- **容器**: Docker + docker-compose
- **运行时**: SNP_Primer_Pipeline3 + BLAST+

## 快速开始

### 开发模式

#### 1. 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

后端 API 文档: http://localhost:8000/docs

#### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

前端访问地址: http://localhost:5173

### 生产部署 (Docker)

```bash
# 构建并启动
docker-compose up --build -d

# 访问服务
# http://localhost:8000
```

## 项目结构

```
kasp_primer_server/
├── backend/              # FastAPI 后端
│   ├── main.py          # 主应用
│   ├── config.py        # 配置
│   ├── genomes.yaml     # 基因组配置
│   └── requirements.txt
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── App.vue     # 主组件
│   │   ├── main.js     # 入口
│   │   └── style.css   # 全局样式
│   └── vite.config.js
├── test_data/           # 测试数据
│   ├── snp_pos_example.txt
│   └── blastdb/
├── Dockerfile
└── docker-compose.yml
```

## API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/genomes` | GET | 获取可用基因组列表 |
| `/api/design` | POST | 提交设计任务 |
| `/api/job/{job_id}` | GET | 查询任务状态/结果 |
| `/api/download/{job_id}/{filename}` | GET | 下载结果文件 |

## 使用示例

### 1. Web UI

1. 打开浏览器访问前端地址
2. 选择参考基因组
3. 点击"加载示例"或手动输入 SNP 坐标
4. 点击"开始设计"
5. 查看结果并下载文件

### 2. API 调用

```bash
# 提交设计任务
curl -X POST http://localhost:8000/api/design \
     -H "Content-Type: application/json" \
     -d '{"snps": "chr7A\t7659\tT\tC\nchr7A\t7716\tA\tG", "genome": "test_reference"}'

# 获取结果 (替换 {job_id})
curl http://localhost:8000/api/job/{job_id}

# 下载文件
curl -O http://localhost:8000/api/download/{job_id}/all_KASP_primers.txt
```

## SNP 输入格式

Tab-分隔的四列格式:

```
Chr     Pos     Ref     Alt
chr7A   7659    T       C
chr7A   7716    A       G
```

## 配置说明

### genomes.yaml

定义可用的参考基因组:

```yaml
genomes:
  - id: test_reference
    name: "Test Reference (小麦测试)"
    path: /data/genomes/test_reference
```

### 环境变量

- `GENOME_CONFIG`: genomes.yaml 文件路径 (默认: `./genomes.yaml`)
- `WORK_DIR`: 任务工作目录 (默认: `/tmp/kasp_jobs`)

## 开发计划

- [x] Phase 1: 基础搭建
- [x] Phase 2: 后端 API 实现
- [x] Phase 3: 前端 UI 实现
- [ ] Phase 4: Docker 集成测试
- [ ] Phase 5: 异步任务处理 (Celery)
- [ ] Phase 6: 结果文件自动清理

## 许可证

本项目基于 MIT 许可证开源。

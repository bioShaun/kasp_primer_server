<template>
  <div id="app" class="app-container">
    <el-container>
    <el-header class="app-header">
      <div class="header-content">
        <div class="header-brand">
          <span class="brand-logo">🧬</span>
          <div class="header-text">
            <h1>KASP Primer Design</h1>
            <p class="header-subtitle">Precision Primer Design for SNP Genotyping</p>
          </div>
        </div>
      </div>
    </el-header>
      
      <el-main class="app-main">
        <el-card class="input-section">
          <template #header>
            <div class="section-header">输入参数</div>
          </template>

          <el-form :model="form" label-width="120px" label-position="left">
            <el-form-item label="参考基因组">
              <el-select v-model="form.genome" placeholder="请选择基因组" style="width: 100%">
                <el-option
                  v-for="genome in genomes"
                  :key="genome.id"
                  :label="genome.name"
                  :value="genome.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="SNP 坐标">
              <div style="width: 100%">
                <div style="margin-bottom: 8px">
                  <el-button size="small" @click="loadExample">📋 加载示例</el-button>
                  <span style="margin-left: 12px; color: #6c757d; font-size: 13px;">
                    格式: Chr\tPos\tRef\tAlt (制表符分隔)
                  </span>
                </div>
                <el-input
                  v-model="form.snps"
                  type="textarea"
                  :rows="8"
                  placeholder="chr7A&#9;7659&#9;T&#9;C&#10;chr7A&#9;7716&#9;A&#9;G"
                />
              </div>
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                @click="submitDesign" 
                :loading="loading"
                :disabled="!form.genome || !form.snps"
              >
                {{ loading ? '设计中...' : '开始设计' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card v-if="results.length > 0 || error" class="result-section">
          <template #header>
            <div class="section-header">设计结果</div>
          </template>

          <el-alert
            v-if="error"
            :title="error"
            type="error"
            show-icon
            :closable="false"
            style="margin-bottom: 16px"
          />

          <div v-if="results.length > 0">
            <el-table :data="results" stripe style="width: 100%" max-height="600" class="results-table">
              <el-table-column prop="Index" label="引物组 ID" width="180" fixed show-overflow-tooltip />
              
              <el-table-column prop="Allele_A" label="等位基因 A 引物" min-width="280">
                <template #default="scope">
                  <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Allele_A)">
                    <code class="primer-code">{{ scope.row.Allele_A }}</code>
                    <span class="tm-tag">{{ scope.row.Tm_A }}°C</span>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="Allele_B" label="等位基因 B 引物" min-width="280">
                <template #default="scope">
                  <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Allele_B)">
                    <code class="primer-code">{{ scope.row.Allele_B }}</code>
                    <span class="tm-tag">{{ scope.row.Tm_B }}°C</span>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="Common" label="通用引物" min-width="280">
                <template #default="scope">
                  <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Common)">
                    <code class="primer-code">{{ scope.row.Common }}</code>
                    <span class="tm-tag">{{ scope.row.Tm_C }}°C</span>
                  </div>
                </template>
              </el-table-column>

              <el-table-column prop="Product_Size" label="大小" width="80" align="center" />
              <el-table-column prop="Genomic_Range" label="范围" width="120" show-overflow-tooltip />
              
              <el-table-column prop="Score" label="评分" width="100" align="center">
                <template #default="scope">
                  <div class="score-container">
                    <el-progress 
                      type="circle" 
                      :percentage="Math.min(parseFloat(scope.row.Score) * 10, 100)" 
                      :width="32" 
                      :stroke-width="3"
                      :color="getScoreColor(scope.row.Score)"
                      :show-text="false"
                    />
                    <span class="score-text">{{ scope.row.Score }}</span>
                  </div>
                </template>
              </el-table-column>
            </el-table>

            <div class="download-section">
              <el-button @click="downloadFile('all_KASP_primers_summary.txt')">
                📥 下载摘要
              </el-button>
              <el-button @click="downloadFile('all_KASP_primers.txt')">
                📥 下载完整结果
              </el-button>
            </div>
          </div>
        </el-card>
        <el-empty 
          v-if="!results.length && !loading && !error" 
          description="准备就绪，开始设计您的引物"
          :image-size="160"
          class="empty-state"
        >
          <template #image>
            <div class="empty-icon">🧬</div>
          </template>
        </el-empty>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const form = ref({
  genome: '',
  snps: ''
})

const genomes = ref([])
const results = ref([])
const loading = ref(false)
const error = ref('')
const currentJobId = ref('')

// 加载基因组列表
onMounted(async () => {
  try {
    const response = await axios.get('/api/genomes')
    genomes.value = response.data
  } catch (err) {
    ElMessage.error('加载基因组列表失败')
  }
})

// 加载示例数据
const loadExample = () => {
  form.value.genome = 'test_reference'
  form.value.snps = 'chr7A\t7659\tT\tC\nchr7A\t7716\tA\tG'
}

// 提交设计任务
const submitDesign = async () => {
  loading.value = true
  error.value = ''
  results.value = []
  
  try {
    const response = await axios.post('/api/design', {
      snps: form.value.snps,
      genome: form.value.genome
    })
    
    const { job_id, status, error: jobError } = response.data
    currentJobId.value = job_id
    
    if (status === 'failed') {
      error.value = jobError || '设计任务失败'
      ElMessage.error('设计失败')
      loading.value = false
    } else {
      // 启动轮询
      pollStatus(job_id)
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '提交失败'
    ElMessage.error('提交失败')
    loading.value = false
  }
}

// 轮询任务状态
const pollStatus = async (jobId) => {
  try {
    const response = await axios.get(`/api/job/${jobId}`)
    const { status, results: jobResults, error: jobError } = response.data
    
    if (status === 'completed') {
      if (jobResults) results.value = jobResults
      loading.value = false
      ElMessage.success('设计完成')
    } else if (status === 'failed') {
      error.value = jobError || '任务执行失败'
      loading.value = false
      ElMessage.error(error.value)
    } else {
      // 继续轮询
      setTimeout(() => pollStatus(jobId), 1000)
    }
  } catch (err) {
    loading.value = false
    ElMessage.error('获取状态失败')
  }
}

// 下载文件
const downloadFile = (filename) => {
  window.open(`/api/download/${currentJobId.value}/${filename}`, '_blank')
}

// 复制到剪贴板
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage({
      message: '已复制到剪贴板',
      type: 'success',
      plain: true,
      duration: 1500
    })
  } catch (err) {
    ElMessage.error('复制失败')
  }
}

// 评分颜色
const getScoreColor = (score) => {
  const s = parseFloat(score)
  if (s >= 7) return '#10b981'
  if (s >= 4) return '#f59e0b'
  return '#ef4444'
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  padding: 12px 0;
  height: auto;
  box-shadow: none;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-logo {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(13, 148, 136, 0.2));
  animation: float 6s ease-in-out infinite;
}

.header-text h1 {
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-weight: 800;
  font-size: 24px;
  background: linear-gradient(135deg, var(--primary-700) 0%, var(--primary-500) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.header-subtitle {
  margin: 2px 0 0;
  color: var(--slate-600);
  font-size: 13px;
  font-weight: 500;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.app-main {
  padding: 32px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.input-section,
.result-section {
  background: var(--glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
  margin-bottom: 32px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.input-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.section-header {
  font-size: 16px;
  font-weight: 700;
  color: var(--slate-900);
  letter-spacing: 0.02em;
}

:deep(.el-card__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  padding: 16px 24px;
}

.download-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  gap: 12px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-500) 100%);
  border: none;
  font-weight: 600;
  height: 40px;
  padding: 0 24px;
  border-radius: 10px;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  background-color: rgba(255, 255, 255, 0.6);
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-family: var(--font-mono);
  font-size: 13px;
  transition: all 0.2s;
}

:deep(.el-input__inner:focus),
:deep(.el-textarea__inner:focus) {
  background-color: #fff;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.15);
}

/* Results Table Styles */
.results-table {
  --el-table-border-color: transparent;
  --el-table-header-bg-color: rgba(0, 0, 0, 0.02);
  background: transparent !important;
}

:deep(.el-table__inner-wrapper::before) {
  display: none;
}

:deep(.el-table tr) {
  background: transparent !important;
}

:deep(.el-table th.el-table__cell) {
  color: var(--slate-600);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.05em;
  padding: 12px 0;
}

:deep(.el-table td.el-table__cell) {
  padding: 12px 0;
}

.primer-sequence-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s;
}

.primer-sequence-box:hover {
  border-color: var(--primary-500);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.primer-code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--slate-900);
  font-weight: 500;
}

.tm-tag {
  font-size: 11px;
  background: var(--primary-50);
  color: var(--primary-700);
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.score-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.score-text {
  font-weight: 700;
  font-size: 13px;
  color: var(--slate-800);
}

.empty-state {
  margin-top: 60px;
}

.empty-icon {
  font-size: 64px;
  filter: grayscale(1);
  opacity: 0.2;
}
</style>

<template>
  <div id="app" class="app-container">
    <el-container>
      <el-header class="app-header">
        <h1>🧬 KASP Primer Design Service</h1>
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
            <el-table :data="results" stripe border style="width: 100%" max-height="500">
              <el-table-column prop="Index" label="引物组 ID" width="180" fixed show-overflow-tooltip />
              <el-table-column prop="Allele_A" label="等位基因 A 引物" min-width="260" show-overflow-tooltip />
              <el-table-column prop="Tm_A" label="Tm A" width="70" />
              <el-table-column prop="Allele_B" label="等位基因 B 引物" min-width="260" show-overflow-tooltip />
              <el-table-column prop="Tm_B" label="Tm B" width="70" />
              <el-table-column prop="Common" label="通用引物" min-width="260" show-overflow-tooltip />
              <el-table-column prop="Tm_C" label="Tm C" width="70" />
              <el-table-column prop="Product_Size" label="产物大小" width="90" />
              <el-table-column prop="Genomic_Range" label="基因组位置" width="120" />
              <el-table-column prop="Score" label="评分" width="70" />
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
    } else if (status === 'completed') {
      await fetchResults(job_id)
      ElMessage.success('设计完成')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || '提交失败'
    ElMessage.error('提交失败')
  } finally {
    loading.value = false
  }
}

// 获取结果
const fetchResults = async (jobId) => {
  try {
    const response = await axios.get(`/api/job/${jobId}`)
    const { status, results: jobResults, error: jobError } = response.data
    
    if (status === 'completed' && jobResults) {
      results.value = jobResults
    } else if (status === 'failed') {
      error.value = jobError || '任务执行失败'
    }
  } catch (err) {
    error.value = '获取结果失败'
  }
}

// 下载文件
const downloadFile = (filename) => {
  window.open(`/api/download/${currentJobId.value}/${filename}`, '_blank')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.app-header {
  background-color: #2c3e50;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.app-main {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.input-section,
.result-section {
  margin-bottom: 24px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
}

.section-header {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
}

.download-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #dee2e6;
}

:deep(.el-button--primary) {
  background-color: #2c3e50;
  border-color: #2c3e50;
  border-radius: 4px;
}

:deep(.el-button--primary:hover) {
  background-color: #3498db;
  border-color: #3498db;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  border-radius: 4px;
  font-family: 'Roboto Mono', monospace;
  font-size: 13px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-table th) {
  background-color: #f8f9fa;
  color: #2c3e50;
  font-weight: 600;
}
</style>

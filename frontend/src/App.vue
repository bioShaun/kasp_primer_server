<template>
  <div id="app" class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="header-brand">
            <!-- Icon removed as requested -->
            <div class="header-text">
              <h1>{{ $t('app.title') }}</h1>
              <p class="header-subtitle">{{ $t('app.subtitle') }}</p>
            </div>
          </div>
          <div class="header-tools">
            <el-radio-group v-model="$i18n.locale" size="small">
              <el-radio-button label="zh">中文</el-radio-button>
              <el-radio-button label="en">EN</el-radio-button>
            </el-radio-group>
          </div>
        </div>
      </el-header>
      
      <el-main class="app-main">
        <!-- Input Section -->
        <InputPanel 
          :genomes="genomes"
          :loading="loading"
          @submit="handleDesignSubmit"
        />

        <!-- Status Section -->
        <JobStatus
          :status="jobStatus"
          :error-message="error"
          :snp-count="snpCount"
          :genome-name="currentGenomeName"
        />

        <!-- Results Section -->
        <transition name="fade">
          <ResultsTable
            v-if="results.length > 0"
            :results="results"
            :job-id="currentJobId"
            @download="handleDownload"
          />
        </transition>

        <!-- Empty State (Intro) -->
        <div v-if="results.length === 0 && jobStatus === 'idle'" class="hero-intro">
          <div class="feature-grid">
            <div class="feature-item">
              <Target class="feature-icon" />
              <h4>{{ $t('app.features.precision') }}</h4>
              <p>{{ $t('app.features.precisionDesc') }}</p>
            </div>
            <div class="feature-item">
              <Zap class="feature-icon" />
              <h4>{{ $t('app.features.fast') }}</h4>
              <p>{{ $t('app.features.fastDesc') }}</p>
            </div>
            <div class="feature-item">
              <BarChart2 class="feature-icon" />
              <h4>{{ $t('app.features.comprehensive') }}</h4>
              <p>{{ $t('app.features.comprehensiveDesc') }}</p>
            </div>
          </div>
        </div>

      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Target, Zap, BarChart2 } from 'lucide-vue-next'
import InputPanel from './components/InputPanel.vue'
import JobStatus from './components/JobStatus.vue'
import ResultsTable from './components/ResultsTable.vue'

const { t } = useI18n()

// State
const genomes = ref([])
const results = ref([])
const loading = ref(false)
const error = ref('')
const currentJobId = ref('')
const jobStatus = ref('idle') // idle, processing, completed, failed

// Context for status display
const snpCount = ref(0)
const currentGenomeId = ref('')

const currentGenomeName = computed(() => {
  const g = genomes.value.find(g => g.id === currentGenomeId.value)
  return g ? g.name : t('status.targetGenome')
})

// Lifecycle
onMounted(async () => {
  try {
    const response = await axios.get('/api/genomes')
    genomes.value = response.data
  } catch (err) {
    ElMessage.error(t('app.loadGenomesError'))
  }
})

// Handlers
const handleDesignSubmit = async (formData) => {
  loading.value = true
  error.value = ''
  results.value = []
  jobStatus.value = 'processing'
  
  // Update context
  currentGenomeId.value = formData.genome
  currentGenomeId.value = formData.genome
  snpCount.value = formData.snps.trim().split('\n').filter(l => l.trim()).length

  try {
    const response = await axios.post('/api/design', {
      snps: formData.snps,
      genome: formData.genome
    })
    
    const { job_id, status, error: jobError } = response.data
    currentJobId.value = job_id
    
    if (status === 'failed') {
      jobStatus.value = 'failed'
      error.value = jobError || t('app.designFailed')
      ElMessage.error(t('app.designFailed'))
      loading.value = false
    } else {
      // Start polling
      pollStatus(job_id)
    }
  } catch (err) {
    jobStatus.value = 'failed'
    error.value = err.response?.data?.detail || t('app.submissionFailed')
    ElMessage.error(t('app.submissionFailed'))
    loading.value = false
  }
}

const pollStatus = async (jobId) => {
  try {
    const response = await axios.get(`/api/job/${jobId}`)
    const { status, results: jobResults, error: jobError } = response.data
    
    if (status === 'completed') {
      if (jobResults) results.value = jobResults
      jobStatus.value = 'completed'
      loading.value = false
      ElMessage.success(t('app.designSuccess'))
    } else if (status === 'failed') {
      jobStatus.value = 'failed'
      error.value = jobError || t('app.designFailed')
      loading.value = false
      ElMessage.error(error.value)
    } else {
      // Continue polling
      setTimeout(() => pollStatus(jobId), 1000)
    }
  } catch (err) {
    loading.value = false
    jobStatus.value = 'failed'
    error.value = t('app.statusCheckFailed')
    ElMessage.error(t('app.statusCheckFailed'))
  }
}

const handleDownload = async (filename) => {
  if (!currentJobId.value) return
  
  try {
    const response = await axios.get(`/api/download/${currentJobId.value}/${filename}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    ElMessage.error(t('app.downloadFailed'))
  }
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
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  padding: 12px 0;
  height: auto;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* brand-logo class removed as explicit element is gone */

.header-text h1 {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 24px;
  color: var(--primary-800);
  margin: 0;
  letter-spacing: -0.02em;
}

.header-subtitle {
  margin: 2px 0 0;
  color: var(--slate-500);
  font-size: 13px;
  font-weight: 500;
}

.app-main {
  padding: 40px 24px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.hero-intro {
  margin-top: 60px;
  text-align: center;
  animation: fadeIn 1s ease;
}

.feature-grid {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-top: 32px;
}

.feature-item {
  color: var(--slate-400);
  transition: all 0.3s;
}

.feature-item:hover {
  color: var(--primary-600);
  transform: translateY(-5px);
}

.feature-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 12px;
}

.feature-item h4 {
  margin: 0 0 4px 0;
  color: var(--slate-600);
}

.feature-item p {
  margin: 0;
  font-size: 13px;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

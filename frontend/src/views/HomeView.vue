<template>
  <div class="home-view">
    <!-- Input Section -->
    <InputPanel 
      :genomes="genomes"
      :loading="loading"
      @submit="handleDesignSubmit"
    />

    <!-- Empty State (Intro) -->
    <div class="hero-intro">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { Target, Zap, BarChart2 } from 'lucide-vue-next'
import InputPanel from '../components/InputPanel.vue'

const { t } = useI18n()
const router = useRouter()

// State
const genomes = ref([])
const loading = ref(false)

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
  
  try {
    const response = await axios.post('/api/design', {
      snps: formData.snps,
      genome: formData.genome
    })
    
    const { job_id, status, error: jobError } = response.data
    
    if (status === 'failed') {
      ElMessage.error(jobError || t('app.designFailed'))
      loading.value = false
    } else {
      // Navigate to results page
      router.push({ name: 'results', params: { jobId: job_id } })
    }
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || t('app.submissionFailed'))
    loading.value = false
  }
}
</script>

<style scoped>
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

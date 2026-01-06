<template>
  <div class="results-view">
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
        :job-id="jobId"
        @download="handleDownload"
      />
    </transition>
    
    <div class="actions" v-if="jobStatus === 'completed' || jobStatus === 'failed'">
      <el-button @click="goHome">{{ $t('app.startDesign') }}</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import JobStatus from '../components/JobStatus.vue'
import ResultsTable from '../components/ResultsTable.vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const jobId = route.params.jobId

// State
const results = ref([])
const error = ref('')
const jobStatus = ref('processing') // init as processing
const snpCount = ref(0)
const genomeName = ref('')
let pollTimer = null

// Computed
const currentGenomeName = computed(() => genomeName.value || t('status.targetGenome'))

// Lifecycle
onMounted(() => {
  pollStatus()
})

onUnmounted(() => {
  if (pollTimer) clearTimeout(pollTimer)
})

// Logic
const pollStatus = async () => {
  try {
    const response = await axios.get(`/api/job/${jobId}`)
    const { status, results: jobResults, error: jobError } = response.data
    
    if (status === 'completed') {
      if (jobResults) {
        results.value = jobResults
        snpCount.value = jobResults.length
      }
      jobStatus.value = 'completed'
      
      const shownKey = `kasp_shown_${jobId}`
      if (!sessionStorage.getItem(shownKey)) {
          ElMessage.success(t('app.designSuccess'))
          sessionStorage.setItem(shownKey, 'true')
      }
    } else if (status === 'failed') {
      jobStatus.value = 'failed'
      error.value = jobError || t('app.designFailed')
      ElMessage.error(error.value)
    } else {
      // Continue polling
      pollTimer = setTimeout(pollStatus, 1000)
    }
  } catch (err) {
    jobStatus.value = 'failed'
    error.value = t('app.statusCheckFailed')
    ElMessage.error(t('app.statusCheckFailed'))
  }
}

const handleDownload = async (filename) => {
  try {
    const response = await axios.get(`/api/download/${jobId}/${filename}`, {
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

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.actions {
  margin-top: 32px;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

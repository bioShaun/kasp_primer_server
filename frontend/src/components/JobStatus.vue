<template>
  <div class="job-status-panel glass-panel" v-if="status && status !== 'idle'">
    <div class="status-content">
      <div class="status-icon-wrapper" :class="status">
        <Loader2 v-if="status === 'processing'" class="spinner-icon spin" />
        <CheckCircle2 v-else-if="status === 'completed'" class="status-icon" />
        <XCircle v-else-if="status === 'failed'" class="status-icon" />
      </div>
      
      <div class="status-text">
        <h3 v-if="status === 'processing'">{{ $t('status.designing') }}</h3>
        <h3 v-else-if="status === 'completed'">{{ $t('status.complete') }}</h3>
        <h3 v-else-if="status === 'failed'">{{ $t('status.failed') }}</h3>
        
        <p v-if="status === 'processing'">{{ $t('status.analyzing', { count: snpCount, genome: genomeName }) }}</p>
        <p v-else-if="status === 'completed'">{{ $t('status.successMsg') }}</p>
        <p v-else-if="status === 'failed'">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { CheckCircle2, XCircle, Loader2 } from 'lucide-vue-next'

defineProps({
  status: {
    type: String,
    required: true, 
    validator: (value) => ['idle', 'processing', 'completed', 'failed'].includes(value)
  },
  errorMessage: {
    type: String,
    default: ''
  },
  snpCount: {
    type: Number,
    default: 0
  },
  genomeName: {
    type: String,
    default: 'Reference'
  }
})
</script>

<style scoped>
.job-status-panel {
  margin: 24px 0;
  padding: 24px;
  background: white;
  border-left: 4px solid transparent;
  transition: all 0.3s ease;
}

.job-status-panel:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.1);
}

.status-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.status-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--slate-100);
}

.status-icon-wrapper.processing {
  background: var(--primary-50);
  color: var(--primary-600);
}

.status-icon-wrapper.completed {
  background: #dcfce7;
  color: #16a34a;
  border: 1px solid #86efac;
}

.status-icon-wrapper.failed {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fca5a5;
}

.status-icon {
  width: 24px;
  height: 24px;
}

.spinner-icon {
  width: 24px;
  height: 24px;
}

.spin {
  animation: spin 1s linear infinite;
}

.status-text h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  color: var(--slate-800);
}

.status-text p {
  margin: 0;
  color: var(--slate-500);
  font-size: 14px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

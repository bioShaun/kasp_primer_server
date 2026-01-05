<template>
  <div class="results-panel glass-panel">
    <div class="panel-header">
      <BarChart3 class="header-icon" />
      <h3>{{ $t('results.title') }}</h3>
      <div class="header-actions">
        <el-button-group>
          <el-button size="small" @click="downloadFile('all_KASP_primers_summary.txt')">
            <Download class="btn-icon" /> {{ $t('results.summary') }}
          </el-button>
          <el-button size="small" type="primary" @click="downloadFile('all_KASP_primers.txt')">
            <Download class="btn-icon" /> {{ $t('results.fullReport') }}
          </el-button>
        </el-button-group>
      </div>
    </div>

    <div class="table-container">
      <el-table 
        :data="results" 
        stripe 
        style="width: 100%" 
        max-height="600" 
        class="results-table"
        :header-cell-style="{ background: 'transparent' }"
      >
        <el-table-column prop="Index" :label="$t('results.id')" width="150" fixed show-overflow-tooltip>
          <template #default="scope">
            <span class="primer-id">{{ scope.row.Index }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="Allele_A" :label="$t('results.alleleA')" min-width="320">
          <template #default="scope">
            <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Allele_A)">
              <code class="primer-code">{{ scope.row.Allele_A }}</code>
              <span class="tm-tag">{{ scope.row.Tm_A }}°C</span>
            </div>
          </template>
        </el-table-column>
  
        <el-table-column prop="Allele_B" :label="$t('results.alleleB')" min-width="320">
          <template #default="scope">
            <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Allele_B)">
              <code class="primer-code">{{ scope.row.Allele_B }}</code>
              <span class="tm-tag">{{ scope.row.Tm_B }}°C</span>
            </div>
          </template>
        </el-table-column>
  
        <el-table-column prop="Common" :label="$t('results.common')" min-width="320">
          <template #default="scope">
            <div class="primer-sequence-box" @click="copyToClipboard(scope.row.Common)">
              <code class="primer-code">{{ scope.row.Common }}</code>
              <span class="tm-tag">{{ scope.row.Tm_C }}°C</span>
            </div>
          </template>
        </el-table-column>
  
        <el-table-column prop="Product_Size" :label="$t('results.size')" width="140" align="center">
          <template #default="scope">
            <span class="size-badge">{{ scope.row.Product_Size }}bp</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="Score" :label="$t('results.quality')" width="120" align="center" fixed="right">
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
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import { BarChart3, Download } from 'lucide-vue-next'

const { t } = useI18n()

const props = defineProps({
  results: {
    type: Array,
    required: true
  },
  jobId: {
    type: String,
    required: true
  }
})

const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    ElMessage({
      message: t('results.copied'),
      type: 'success',
      plain: true,
      duration: 1500
    })
  } catch (err) {
    ElMessage.error(t('results.copyFailed'))
  }
}

const getScoreColor = (score) => {
  const s = parseFloat(score)
  if (s >= 7) return '#10b981'
  if (s >= 4) return '#f59e0b'
  return '#ef4444'
}

const emit = defineEmits(['download'])

const downloadFile = (filename) => {
  emit('download', filename)
}
</script>

<style scoped>
.results-panel {
  padding: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-top: 24px;
}

.panel-header {
  padding: 16px 24px;
  background: var(--slate-50);
  border-bottom: 1px solid var(--slate-200);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--slate-800);
  flex-grow: 1;
  margin-left: 12px;
}

.header-icon {
  width: 20px;
  height: 20px;
  color: var(--slate-600);
}

.btn-icon {
  width: 14px;
  height: 14px;
  margin-right: 6px;
}

.results-table {
  --el-table-border-color: var(--slate-100);
  --el-table-header-bg-color: transparent;
}

:deep(.el-table th.el-table__cell) {
  background-color: white !important;
  color: var(--slate-500);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 12px 16px;
}

:deep(.el-table td.el-table__cell) {
  padding: 12px 16px;
}

.primer-id {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--primary-700);
}

.primer-sequence-box {
  background: var(--slate-50);
  border: 1px solid var(--slate-200);
  border-radius: 6px;
  padding: 4px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s;
}

.primer-sequence-box:hover {
  border-color: var(--primary-400);
  background: white;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.primer-code {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--slate-700);
}

.tm-tag {
  font-size: 10px;
  background: white;
  border: 1px solid var(--slate-200);
  padding: 2px 4px;
  border-radius: 4px;
  color: var(--slate-500);
}

.size-badge {
  background: var(--slate-100);
  color: var(--slate-600);
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.score-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-text {
  font-weight: 700;
  font-size: 13px;
  color: var(--slate-800);
}
</style>

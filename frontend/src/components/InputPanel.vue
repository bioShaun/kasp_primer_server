<template>
  <div class="input-panel glass-panel">
    <div class="panel-header">
      <Dna class="header-icon" />
      <h3>{{ $t('input.title') }}</h3>
    </div>
    
    <div class="input-content">
      <el-form :model="form" label-width="120px" label-position="top">
        
        <!-- Genome Selection -->
        <el-form-item :label="$t('input.reference')">
          <el-select v-model="form.genome" :placeholder="$t('input.selectGenome')" class="scientific-select">
            <template #prefix>
              <Dna class="input-prefix-icon" />
            </template>
            <el-option
              v-for="genome in genomes"
              :key="genome.id"
              :label="genome.name"
              :value="genome.id"
            />
          </el-select>
        </el-form-item>

        <!-- SNP Input Method Tabs -->
        <div class="input-method-tabs">
          <div 
            class="method-tab" 
            :class="{ active: inputMethod === 'text' }"
            @click="inputMethod = 'text'"
          >
            <Edit3 class="tab-icon" />
            <span class="tab-label">{{ $t('input.pasteCoords') }}</span>
          </div>
          <div 
            class="method-tab" 
            :class="{ active: inputMethod === 'file' }"
            @click="inputMethod = 'file'"
          >
            <FolderOpen class="tab-icon" />
            <span class="tab-label">{{ $t('input.uploadFile') }}</span>
          </div>
        </div>

        <!-- Text Input Area -->
        <div v-if="inputMethod === 'text'" class="input-area fade-in">
          <div class="area-header">
            <span class="helper-text">{{ $t('input.formatHelper') }}</span>
            <el-button link type="primary" size="small" @click="loadExample">{{ $t('input.loadExample') }}</el-button>
          </div>
          <el-input
            v-model="form.snps"
            type="textarea"
            :rows="8"
            :placeholder="$t('input.placeholder')"
            class="scientific-input"
          />
        </div>

        <!-- File Upload Area -->
        <div v-else class="input-area fade-in">
          <div 
            class="upload-zone"
            :class="{ 'is-dragover': isDragOver, 'has-file': fileName }"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleDrop"
            @click="triggerFileInput"
          >
            <input 
              type="file" 
              ref="fileInput" 
              class="hidden-input" 
              accept=".txt,.tsv,.csv"
              @change="handleFileSelect"
            >
            <div class="upload-content" v-if="!fileName">
              <CloudUpload class="upload-icon" />
              <p>{{ $t('input.dragDrop') }}</p>
              <p class="sub-text">{{ $t('input.browse') }}</p>
            </div>
            <div class="file-content" v-else>
              <FileText class="file-icon" />
              <div class="file-info">
                <span class="file-name">{{ fileName }}</span>
                <span class="file-size">{{ fileSize }}</span>
              </div>
              <el-button 
                type="danger" 
                link 
                icon="Delete" 
                @click.stop="clearFile"
                class="remove-file-btn"
              />
            </div>
          </div>
          <div class="file-preview" v-if="fileName">
            <span class="preview-label">{{ $t('input.preview') }}</span>
            <pre class="preview-content">{{ filePreview }}</pre>
          </div>
        </div>

        <div class="action-bar">
          <el-button 
            type="primary" 
            size="large"
            class="submit-btn"
            @click="handleSubmit" 
            :loading="loading"
            :disabled="!isValid"
          >
            {{ loading ? $t('input.running') : $t('input.submit') }}
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dna, Edit3, FolderOpen, CloudUpload, FileText } from 'lucide-vue-next'

const props = defineProps({
  genomes: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const inputMethod = ref('text')
const form = ref({
  genome: '',
  snps: ''
})

// File Upload State
const fileInput = ref(null)
const isDragOver = ref(false)
const fileName = ref('')
const fileSize = ref('')
const filePreview = ref('')

const isValid = computed(() => {
  return form.value.genome && form.value.snps
})

const loadExample = () => {
  form.value.genome = 'test_reference'
  form.value.snps = 'chr7A\t7659\tT\tC\nchr7A\t7716\tA\tG'
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleDrop = (e) => {
  isDragOver.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const handleFileSelect = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const processFile = (file) => {
  fileName.value = file.name
  fileSize.value = formatFileSize(file.size)
  
  const reader = new FileReader()
  reader.onload = (e) => {
    const text = e.target.result
    form.value.snps = text
    
    // Generate preview
    const lines = text.split('\n').filter(l => l.trim())
    filePreview.value = lines.slice(0, 5).join('\n') + (lines.length > 5 ? '\n...' : '')
  }
  reader.readAsText(file)
}

const clearFile = () => {
  fileName.value = ''
  fileSize.value = ''
  filePreview.value = ''
  form.value.snps = ''
  if (fileInput.value) fileInput.value.value = ''
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleSubmit = () => {
  emit('submit', form.value)
}
</script>

<style scoped>
.input-panel {
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--slate-100);
  padding-bottom: 16px;
}

.header-icon {
  width: 40px;
  height: 40px;
  background: var(--primary-50);
  padding: 8px;
  border-radius: 8px;
  color: var(--primary-600);
}

.panel-header h3 {
  margin: 0;
  color: var(--slate-800);
  font-size: 18px;
  font-weight: 600;
}

.scientific-select {
  width: 100%;
}

:deep(.scientific-select .el-input__wrapper) {
  background-color: var(--slate-50);
  box-shadow: none !important;
  border: 1px solid var(--slate-200);
  padding-left: 12px;
}

:deep(.scientific-select .el-input__wrapper.is-focus) {
  border-color: var(--primary-500);
  background-color: white;
  box-shadow: 0 0 0 1px var(--primary-500) !important;
}

.input-prefix-icon {
  width: 14px;
  height: 14px;
  color: var(--slate-500);
}

.input-method-tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  background: var(--slate-50);
  padding: 4px;
  border-radius: 8px;
}

.method-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  color: var(--slate-500);
  font-weight: 500;
  font-size: 14px;
}

.method-tab:hover {
  background: rgba(255, 255, 255, 0.5);
  color: var(--slate-700);
}

.method-tab.active {
  background: white;
  color: var(--primary-600);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-weight: 600;
}

.tab-icon {
  width: 16px;
  height: 16px;
}

.area-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.helper-text {
  font-size: 12px;
  color: var(--slate-500);
  font-family: var(--font-mono);
}

.scientific-input :deep(.el-textarea__inner) {
  font-family: var(--font-mono);
  background-color: var(--slate-50);
  border: 1px solid var(--slate-200);
  padding: 12px;
  font-size: 13px;
  line-height: 1.6;
}

.scientific-input :deep(.el-textarea__inner:focus) {
  background-color: white;
  border-color: var(--primary-500);
}

.upload-zone {
  border: 2px dashed var(--slate-200);
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  background: var(--slate-50);
  color: var(--slate-500);
  cursor: pointer;
  transition: all 0.2s;
}

.upload-zone:hover {
  border-color: var(--primary-400);
  background: var(--primary-50);
  color: var(--primary-700);
}

.upload-icon {
  width: 32px;
  height: 32px;
  margin-bottom: 8px;
}

.hidden-input {
  display: none;
}

.upload-zone.is-dragover {
  border-color: var(--primary-500);
  background: var(--primary-50);
  transform: scale(1.02);
}

.upload-zone.has-file {
  border-style: solid;
  border-color: var(--primary-200);
  background: white;
  padding: 16px;
}

.file-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.file-icon {
  width: 32px;
  height: 32px;
}

.file-info {
  flex: 1;
  text-align: left;
}

.file-name {
  display: block;
  font-weight: 600;
  color: var(--slate-800);
  font-size: 14px;
}

.file-size {
  display: block;
  color: var(--slate-500);
  font-size: 12px;
}

.file-preview {
  margin-top: 16px;
  background: var(--slate-50);
  border-radius: 8px;
  padding: 12px;
  text-align: left;
}

.preview-label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: var(--slate-500);
  text-transform: uppercase;
  margin-bottom: 8px;
}

.preview-content {
  margin: 0;
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--slate-600);
  line-height: 1.5;
  overflow-x: auto;
}

.action-bar {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.submit-btn {
  width: 100%;
  font-weight: 600;
  letter-spacing: 0.02em;
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-500) 100%);
  border: none;
  height: 48px;
}

.submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
}

.fade-in {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

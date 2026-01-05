<template>
  <div id="app" class="app-container">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="header-brand" @click="$router.push('/')" style="cursor: pointer">
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
        <router-view></router-view>
      </el-main>

      <el-footer class="app-footer">
        <div class="footer-content">
          <span class="footer-text">{{ $t('app.poweredBy') }}</span>
          <a href="https://github.com/pinbo/SNP_Primer_Pipeline2" target="_blank" rel="noopener noreferrer" class="footer-link">
            <Github class="footer-icon" />
            SNP_Primer_Pipeline2
          </a>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { Github } from 'lucide-vue-next'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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
  flex: 1;
}

.app-footer {
  padding: 24px 0;
  color: var(--slate-400);
  font-size: 13px;
  text-align: center;
  border-top: 1px solid var(--slate-100);
  background: white;
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.footer-text {
  color: var(--slate-500);
}

.footer-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--slate-700);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
  padding: 4px 8px;
  border-radius: 6px;
  background: var(--slate-50);
}

.footer-link:hover {
  color: var(--primary-700);
  background: var(--primary-50);
}

.footer-icon {
  width: 14px;
  height: 14px;
}
</style>

# UI Optimization - AI 执行文档 (v2 - Advanced)

> 本文档基于 `design-doc/ui_optimization.md`，为 AI 助手提供可直接执行的**分步指令**。旨在打造**Premium**级别的科研工具界面。

---

## 0. 前置条件

| 检查项 | 说明 | 验证命令 |
|--------|------|----------|
| 前端目录 | 存在 `frontend/src/` | `ls frontend/src/` |
| 依赖检查 | 确保 `element-plus` 已安装 | `npm list element-plus` |

---

## Phase 1: 高级设计系统 (CSS Variables)

### 1.1 定义现代色彩与阴影

**文件**: `frontend/src/style.css`

引入更显高级的**Mesh Gradient**背景和**Glassmorphism**变量：

```css
:root {
  /* Brand Colors - Modern Teal/Emerald */
  --primary-50: #f0fdfa;
  --primary-100: #ccfbf1;
  --primary-500: #14b8a6;
  --primary-600: #0d9488;
  --primary-700: #0f766e;
  --primary-900: #134e4a;
  
  /* Neutral scale for UI */
  --slate-50: #f8fafc;
  --slate-100: #f1f5f9;
  --slate-400: #94a3b8;
  --slate-600: #475569;
  --slate-800: #1e293b;
  --slate-900: #0f172a;

  /* Functional Colors */
  --c-success: #10b981;
  --c-warning: #f59e0b;
  --c-error: #ef4444;
  --c-bg-gradient: radial-gradient(at 0% 0%, hsla(168,83%,94%,1) 0, transparent 50%), radial-gradient(at 50% 0%, hsla(196,75%,96%,1) 0, transparent 50%), radial-gradient(at 100% 0%, hsla(168,83%,94%,1) 0, transparent 50%);
  
  /* Effects */
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-border: 1px solid rgba(255, 255, 255, 0.5);
  --glass-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  --backdrop-blur: blur(12px);
  
  /* Allele Colors (Soft Badges) */
  --badge-a-bg: #ecfdf5; --badge-a-text: #047857;
  --badge-t-bg: #fef2f2; --badge-t-text: #b91c1c;
  --badge-g-bg: #eff6ff; --badge-g-text: #1d4ed8;
  --badge-c-bg: #fffbeb; --badge-c-text: #b45309;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: #f8fafc;
  background-image: var(--c-bg-gradient);
  background-attachment: fixed; /* Parallax effect */
  color: var(--slate-800);
  min-height: 100vh;
}
```

---

## Phase 2: 沉浸式 Header 设计

### 2.1 创建透明磨砂 Header

**文件**: `frontend/src/App.vue`

使用 `backdrop-filter` 实现磨砂玻璃效果，并添加渐变文字：

```css
.app-header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
  padding: 16px 0;
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
  font-size: 26px;
  background: linear-gradient(135deg, var(--primary-700) 0%, var(--primary-500) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}
```

---

## Phase 3: 卡片与交互优化 (Glassmorphism)

### 3.1 悬浮卡片效果

**文件**: `frontend/src/App.vue`

```css
.input-section, .result-section {
  background: var(--glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 16px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.02),
    0 20px 25px -5px rgba(0, 0, 0, 0.05); /* Deep shadow */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden; /* For inner border radius */
}

.input-section:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 10px 15px -3px rgba(0, 0, 0, 0.05),
    0 4px 6px -2px rgba(0, 0, 0, 0.025);
}
```

### 3.2 现代化输入框

```css
:deep(.el-textarea__inner) {
  background-color: rgba(255, 255, 255, 0.6);
  border: 1px solid #e2e8f0;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
  transition: all 0.2s;
}

:deep(.el-textarea__inner:focus) {
  background-color: #fff;
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.15); /* Focus ring */
}
```

---

## Phase 4: 极简主义表格

### 4.1 无边框清爽设计

**文件**: `frontend/src/App.vue`

去除繁杂的表格边框，增加行间距和圆角：

```css
:deep(.el-table) {
  --el-table-border-color: transparent;
  --el-table-header-bg-color: transparent;
  background: transparent !important;
}

:deep(.el-table tr) {
  background: transparent !important;
}

:deep(.el-table th.el-table__cell) {
  background: transparent;
  color: var(--slate-600);
  font-weight: 600;
  letter-spacing: 0.02em;
  border-bottom: 2px solid #e2e8f0;
}

:deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid #f1f5f9;
}

/* 序列代码块优化 */
.primer-sequence-box {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 4px 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  group: hover .copy-btn { opacity: 1; }
}

.primer-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--slate-800);
}
```

### 4.2 评分可视化 (Progress Ring)

不只是显示数字，增加视觉反馈：

```vue
<template #default="scope">
  <div class="score-container">
    <el-progress 
      type="circle" 
      :percentage="parseFloat(scope.row.Score) * 10" 
      :width="32" 
      :stroke-width="3"
      :color="getScoreColor(scope.row.Score)"
      :show-text="false"
    />
    <span class="score-text">{{ scope.row.Score }}</span>
  </div>
</template>

<style scoped>
.score-container {
  display: flex;
  align-items: center;
  gap: 8px;
}
.score-text {
  font-weight: 600;
  font-size: 13px;
}
</style>
```

---

## Phase 5: 空状态与微交互

### 5.1 数据为空时的插画

当没有数据时，显示优雅的空状态：

```vue
<el-empty 
  v-if="!results.length && !loading && !error" 
  description="Ready to design primers"
  :image-size="120"
>
  <template #image>
    <!-- 使用自定义 SVG 或 Element 默认 -->
    <img src="/vite.svg" style="opacity: 0.2; filter: grayscale(100%);" />
  </template>
</el-empty>
```

### 5.2 复制交互提示

为序列添加点击复制功能和提示：

```javascript
/* 逻辑代码示例 */
import { useClipboard } from '@vueuse/core' // 需要安装或手写 copy
// ...
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text);
    ElMessage.success({ message: 'Copied!', plain: true, duration: 1500 });
  } catch (err) {
    console.error('Copy failed', err);
  }
}
```

---

## 执行检查清单

| Phase | 任务 | 状态 |
|-------|------|------|
| 1 | 定义 Mesh Gradient 背景变量 | [ ] |
| 2 | 实现 Glassmorphism Header | [ ] |
| 3 | 应用卡片悬浮与阴影效果 | [ ] |
| 4 | 极简表格样式 (去边框) | [ ] |
| 4 | 评分圆形进度条组件 | [ ] |
| 5 | 准备就绪空状态界面 | [ ] |

---

## 验证与验收

运行 `npm run dev` 并观察：
1.  **背景**：是否呈现柔和的极光渐变？
2.  **滚动**：Header 是否固定且有磨砂模糊效果？
3.  **质感**：卡片是否像悬浮的毛玻璃？
4.  **清晰度**：表格无纵向边框，阅读是否更流畅？

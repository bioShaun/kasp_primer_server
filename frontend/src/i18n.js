import { createI18n } from 'vue-i18n'

const messages = {
    zh: {
        app: {
            title: 'KASP 引物设计',
            subtitle: '为 SNP 分型提供的精准引物设计服务',
            loadingGenomes: '正在加载基因组...',
            loadGenomesError: '加载基因组失败',
            designSuccess: '设计完成',
            designFailed: '设计失败',
            submissionFailed: '提交失败',
            statusCheckFailed: '状态查询失败',
            downloadFailed: '下载失败',
            runningAnalysis: '正在运行分析...',
            startDesign: '开始引物设计',
            features: {
                precision: '精准',
                precisionDesc: '针对高特异性进行优化',
                fast: '快速',
                fastDesc: '后端并行处理',
                comprehensive: '全面',
                comprehensiveDesc: '完整的热力学分析'
            },
            poweredBy: '核心算法基于开源项目'
        },
        input: {
            title: '设计参数',
            reference: '参考基因组',
            selectGenome: '选择目标基因组',
            pasteCoords: '粘贴坐标',
            uploadFile: '上传文件',
            formatHelper: '格式: Chr\\tPos\\tRef\\tAlt (制表符分隔)',
            loadExample: '加载示例',
            placeholder: 'chr7A\t7659\tT\tC\nchr7A\t7716\tA\tG',
            dragDrop: '将坐标文件拖拽至此处',
            browse: '或点击进行浏览',
            preview: '预览 (前 5 行):',
            running: '正在运行分析...',
            submit: '开始引物设计'
        },
        status: {
            designing: '正在设计引物...',
            complete: '设计完成！',
            failed: '设计失败',
            analyzing: '正在根据 {genome} 分析 {count} 个 SNP',
            successMsg: '已成功为您的目标生成引物。',
            targetGenome: '目标基因组'
        },
        results: {
            title: '设计结果',
            summary: '摘要 (.txt)',
            fullReport: '完整报告 (.txt)',
            id: '编号',
            alleleA: '等位基因 A',
            alleleB: '等位基因 B',
            common: '通用引物',
            size: '产物长度',
            quality: '质量',
            copied: '已复制到剪贴板',
            copyFailed: '复制失败'
        }
    },
    en: {
        app: {
            title: 'KASP Primer Design',
            subtitle: 'Precision Primer Design for SNP Genotyping',
            loadingGenomes: 'Loading genomes...',
            loadGenomesError: 'Failed to load genomes',
            designSuccess: 'Design Complete',
            designFailed: 'Design Failed',
            submissionFailed: 'Submission Failed',
            statusCheckFailed: 'Status Check Failed',
            downloadFailed: 'Download Failed',
            runningAnalysis: 'Running Analysis...',
            startDesign: 'Start Design Pipeline',
            features: {
                precision: 'Precision',
                precisionDesc: 'Optimized for high specificity',
                fast: 'Fast',
                fastDesc: 'Parallelized backend processing',
                comprehensive: 'Comprehensive',
                comprehensiveDesc: 'Full thermodynamic analysis'
            },
            poweredBy: 'Core algorithm based on open-source project'
        },
        input: {
            title: 'Design Parameters',
            reference: 'Reference Genome',
            selectGenome: 'Select Target Genome',
            pasteCoords: 'Paste Coordinates',
            uploadFile: 'Upload File',
            formatHelper: 'Format: Chr\\tPos\\tRef\\tAlt (Tab-separated)',
            loadExample: 'Load Example',
            placeholder: 'chr7A\t7659\tT\tC\nchr7A\t7716\tA\tG',
            dragDrop: 'Drag & drop your Coordinate file here',
            browse: 'or click to browse',
            preview: 'Preview (First 5 lines):',
            running: 'Running Analysis...',
            submit: 'Start Design Pipeline'
        },
        status: {
            designing: 'Designing Primers...',
            complete: 'Design Complete!',
            failed: 'Design Failed',
            analyzing: 'Analyzing {count} SNPs against {genome}',
            successMsg: 'Successfully generated primers for your targets.',
            targetGenome: 'Target Genome'
        },
        results: {
            title: 'Design Results',
            summary: 'Summary (.txt)',
            fullReport: 'Full Report (.txt)',
            id: 'ID',
            alleleA: 'Allele A',
            alleleB: 'Allele B',
            common: 'Common Primer',
            size: 'Size',
            quality: 'Quality',
            copied: 'Copied to clipboard',
            copyFailed: 'Failed to copy'
        }
    }
}

const i18n = createI18n({
    legacy: false, // Vue 3 Composition API
    locale: 'zh', // Default language
    fallbackLocale: 'en',
    messages
})

export default i18n

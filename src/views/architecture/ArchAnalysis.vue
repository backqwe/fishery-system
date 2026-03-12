<template>
  <div class="arch-analysis">
    <!-- 页面标题 -->
    <el-card shadow="never" class="page-header-card">
      <div class="page-header">
        <div class="header-text">
          <h2 class="page-title">
            <el-icon color="#409eff" size="22"><DataAnalysis /></el-icon>
            新型弹性架构可扩展性与可伸缩性对比分析
          </h2>
          <p class="page-desc">
            本系统架构经历三种形态演化：单体模式（图18）→ 中间模式（图19）→ 完全微服务模式（图20），
            兼具可扩展性（功能扩展）与可伸缩性（性能扩容），本页面对其进行学术建模与量化对比分析。
          </p>
        </div>
      </div>
    </el-card>

    <!-- 三种架构形态演化对比 -->
    <el-card shadow="hover" class="section-card">
      <template #header>
        <div class="section-header">
          <span class="section-title">
            <el-icon color="#409eff"><Grid /></el-icon>
            架构演化形态对比（图18 / 图19 / 图20）
          </span>
          <el-tag type="info" size="small">架构演化路径</el-tag>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :xs="24" :md="8" v-for="arch in archForms" :key="arch.id">
          <div class="arch-card" :class="arch.colorClass">
            <div class="arch-card-header">
              <div class="arch-badge">图{{ arch.figureNum }}</div>
              <div class="arch-icon-wrap">
                <el-icon size="32" :color="arch.iconColor"><component :is="arch.icon" /></el-icon>
              </div>
              <div class="arch-title">{{ arch.title }}</div>
              <div class="arch-subtitle">{{ arch.subtitle }}</div>
            </div>
            <div class="arch-layers">
              <div
                class="arch-layer"
                v-for="layer in arch.layers"
                :key="layer.name"
                :style="{ background: layer.bg, borderColor: layer.border }"
              >
                <span class="layer-name">{{ layer.name }}</span>
                <span class="layer-desc">{{ layer.desc }}</span>
              </div>
            </div>
            <div class="arch-metrics">
              <div class="metric" v-for="m in arch.metrics" :key="m.label">
                <span class="metric-label">{{ m.label }}</span>
                <el-progress
                  :percentage="m.value"
                  :color="m.color"
                  :stroke-width="8"
                  :show-text="false"
                />
                <span class="metric-val">{{ m.display }}</span>
              </div>
            </div>
            <div class="arch-pros-cons">
              <div class="pros" v-if="arch.pros.length">
                <span class="pros-label">✅ 优势</span>
                <ul>
                  <li v-for="p in arch.pros" :key="p">{{ p }}</li>
                </ul>
              </div>
              <div class="cons" v-if="arch.cons.length">
                <span class="cons-label">⚠️ 局限</span>
                <ul>
                  <li v-for="c in arch.cons" :key="c">{{ c }}</li>
                </ul>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
      <!-- 演化箭头 -->
      <div class="evolution-arrow">
        <span class="arrow-label">架构演化方向</span>
        <div class="arrow-line">
          <span class="arrow-node">单体（图18）</span>
          <span class="arrow-sep">→ 渐进迁移 →</span>
          <span class="arrow-node">中间态（图19）</span>
          <span class="arrow-sep">→ 完全拆分 →</span>
          <span class="arrow-node active">微服务（图20）</span>
        </div>
      </div>
    </el-card>

    <!-- 迁移复杂度数学建模 -->
    <el-row :gutter="16">
      <el-col :xs="24" :lg="14">
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon color="#e6a23c"><TrendCharts /></el-icon>
                迁移复杂度数学建模：C = f(M, N)
              </span>
            </div>
          </template>

          <!-- 公式说明 -->
          <div class="formula-block">
            <div class="formula-title">加权线性模型</div>
            <div class="formula-main">C = α·M + β·N</div>
            <div class="formula-vars">
              <div class="var-item">
                <span class="var-name">M</span>
                <span class="var-desc">迁移组件数（需提取/重构的现有模块数量）</span>
              </div>
              <div class="var-item">
                <span class="var-name">N</span>
                <span class="var-desc">新增组件数（网关、注册中心、RPC等需新建数量）</span>
              </div>
              <div class="var-item">
                <span class="var-name">α</span>
                <span class="var-desc">迁移权重（耦合度越高α越大，当前取 1.2）</span>
              </div>
              <div class="var-item">
                <span class="var-name">β</span>
                <span class="var-desc">新增权重（组件复杂度越高β越大，当前取 1.5）</span>
              </div>
            </div>
            <div class="formula-title mt-16">对数归一化模型</div>
            <div class="formula-main">C = log(M+1) + log(N+1)</div>
            <div class="formula-note">
              对数模型可消除异常值影响，更适合大规模系统迁移的相对比较场景。
            </div>
          </div>

          <!-- 对比示例 -->
          <div class="compare-table-wrap">
            <div class="compare-title">典型场景量化对比（10模块系统）</div>
            <el-table :data="compareData" border stripe size="small" class="compare-table">
              <el-table-column prop="scenario" label="迁移场景" min-width="140" />
              <el-table-column prop="M" label="M（迁移组件）" width="110" align="center" />
              <el-table-column prop="N" label="N（新增组件）" width="110" align="center" />
              <el-table-column prop="C_linear" label="C（线性模型）" width="120" align="center">
                <template #default="{ row }">
                  <span :class="row.isNew ? 'value-low' : 'value-high'">{{ row.C_linear }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="C_log" label="C（对数模型）" width="120" align="center">
                <template #default="{ row }">
                  <span :class="row.isNew ? 'value-low' : 'value-high'">{{ row.C_log }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="reduction" label="复杂度降低" width="100" align="center">
                <template #default="{ row }">
                  <el-tag :type="row.isNew ? 'success' : 'danger'" size="small">{{ row.reduction }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>

      <!-- 迁移复杂度随规模变化折线图 -->
      <el-col :xs="24" :lg="10">
        <el-card shadow="hover" class="section-card chart-section">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon color="#67c23a"><DataLine /></el-icon>
                迁移复杂度 C 随模块规模 M 增长趋势
              </span>
            </div>
          </template>
          <div ref="complexityChartRef" class="chart-container"></div>
          <div class="chart-legend">
            <span class="legend-item legend-red">● 传统全拆分架构</span>
            <span class="legend-item legend-blue">● 本新型弹性架构</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 可伸缩性对比分析 -->
    <el-row :gutter="16">
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon color="#f56c6c"><ScaleToOriginal /></el-icon>
                可伸缩性（性能扩容）对比
              </span>
            </div>
          </template>
          <div ref="scalabilityChartRef" class="chart-container"></div>
          <div class="scalability-desc">
            <el-alert
              title="传统单体扩容：仅支持整体水平扩容，粒度粗，资源浪费，无法针对单一业务瓶颈细粒度伸缩。"
              type="warning"
              :closable="false"
              show-icon
              style="margin-bottom:8px"
            />
            <el-alert
              title="本架构扩容：支持业务模块独立横向扩容，哪个功能瓶颈就扩哪个，资源利用率高、性能扩容精准。"
              type="success"
              :closable="false"
              show-icon
            />
          </div>
        </el-card>
      </el-col>

      <!-- 可扩展性对比 -->
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon color="#909399"><Connection /></el-icon>
                可扩展性（功能扩展）渐进迁移优势
              </span>
            </div>
          </template>
          <div ref="extensibilityChartRef" class="chart-container"></div>
          <div class="extensibility-steps">
            <el-steps :active="3" align-center size="small" class="migration-steps">
              <el-step title="图18：单体模式" description="所有模块耦合，M=10，N=5" />
              <el-step title="图19：中间模式" description="逐步拆分业务层，M可从1开始渐进" />
              <el-step title="图20：完全微服务" description="基础层/网关提前存在，N趋于0" />
            </el-steps>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 综合评估结论 -->
    <el-card shadow="hover" class="section-card conclusion-card">
      <template #header>
        <div class="section-header">
          <span class="section-title">
            <el-icon color="#409eff"><Finished /></el-icon>
            综合评估结论
          </span>
        </div>
      </template>
      <el-row :gutter="16">
        <el-col :xs="24" :md="8" v-for="c in conclusions" :key="c.title">
          <div class="conclusion-item" :class="c.colorClass">
            <div class="con-icon">
              <el-icon size="28" :color="c.iconColor"><component :is="c.icon" /></el-icon>
            </div>
            <div class="con-title">{{ c.title }}</div>
            <div class="con-detail">{{ c.detail }}</div>
            <div class="con-badge">
              <el-tag :type="c.tagType" effect="dark" size="small">{{ c.badge }}</el-tag>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// ─── 架构形态数据 ────────────────────────────────────────────────
const archForms = [
  {
    id: 1,
    figureNum: 18,
    title: '单体模式',
    subtitle: '传统架构 · 紧耦合',
    icon: 'Box',
    iconColor: '#f56c6c',
    colorClass: 'arch-monolith',
    layers: [
      { name: '表现层', desc: 'Web/App UI', bg: '#fff2f2', border: '#fbc4c4' },
      { name: '业务层', desc: '所有业务逻辑耦合', bg: '#fff2f2', border: '#fbc4c4' },
      { name: '数据层', desc: '共用数据库', bg: '#fff2f2', border: '#fbc4c4' }
    ],
    metrics: [
      { label: '部署耦合度', value: 95, display: '极高', color: '#f56c6c' },
      { label: '迁移复杂度', value: 90, display: '极高', color: '#f56c6c' },
      { label: '伸缩灵活性', value: 15, display: '极低', color: '#f56c6c' }
    ],
    pros: ['开发简单', '初期成本低'],
    cons: ['模块全耦合', '迁移成本高', '只能整体扩容', '单点故障风险']
  },
  {
    id: 2,
    figureNum: 19,
    title: '中间模式',
    subtitle: '本架构 · 渐进迁移态',
    icon: 'Connection',
    iconColor: '#e6a23c',
    colorClass: 'arch-middle',
    layers: [
      { name: '网关层', desc: 'API Gateway（已存在）', bg: '#fdf6ec', border: '#f5dab1' },
      { name: '业务层（已迁移）', desc: '部分业务微服务化', bg: '#fdf6ec', border: '#f5dab1' },
      { name: '业务层（待迁移）', desc: '剩余业务仍在原处', bg: '#fff8e6', border: '#fcd787' },
      { name: '基础层', desc: '公共服务（已存在）', bg: '#fdf6ec', border: '#f5dab1' }
    ],
    metrics: [
      { label: '部署耦合度', value: 45, display: '中等', color: '#e6a23c' },
      { label: '迁移复杂度', value: 40, display: '可控', color: '#e6a23c' },
      { label: '伸缩灵活性', value: 65, display: '较高', color: '#67c23a' }
    ],
    pros: ['渐进式迁移', '边界清晰', '网关/基础层复用', 'M可从1开始'],
    cons: ['过渡期需维护两套部署', '过渡期整体架构复杂性增加']
  },
  {
    id: 3,
    figureNum: 20,
    title: '完全微服务模式',
    subtitle: '目标架构 · 解耦完成',
    icon: 'Share',
    iconColor: '#67c23a',
    colorClass: 'arch-micro',
    layers: [
      { name: '网关层', desc: 'API Gateway', bg: '#f0f9eb', border: '#b3e19d' },
      { name: '监测服务', desc: '实时监测微服务', bg: '#f0f9eb', border: '#b3e19d' },
      { name: '分析服务', desc: '历史/预测微服务', bg: '#f0f9eb', border: '#b3e19d' },
      { name: '管理服务', desc: '基础信息微服务', bg: '#f0f9eb', border: '#b3e19d' },
      { name: '基础层', desc: '注册中心/配置中心', bg: '#f0f9eb', border: '#b3e19d' }
    ],
    metrics: [
      { label: '部署耦合度', value: 10, display: '极低', color: '#67c23a' },
      { label: '迁移复杂度', value: 20, display: '最低', color: '#67c23a' },
      { label: '伸缩灵活性', value: 95, display: '极高', color: '#67c23a' }
    ],
    pros: ['独立部署', '按需扩容', '故障隔离', '技术栈灵活'],
    cons: ['分布式复杂性']
  }
]

// ─── 迁移复杂度对比数据 ────────────────────────────────────────
const compareData = [
  {
    scenario: '传统全拆分（一次性）',
    M: 10,
    N: 5,
    C_linear: (1.2 * 10 + 1.5 * 5).toFixed(1),
    C_log: (Math.log(11) + Math.log(6)).toFixed(2),
    reduction: '基准',
    isNew: false
  },
  {
    scenario: '本架构·第1次迁移',
    M: 1,
    N: 0,
    C_linear: (1.2 * 1 + 1.5 * 0).toFixed(1),
    C_log: (Math.log(2) + Math.log(1)).toFixed(2),
    reduction: '↓ 94%',
    isNew: true
  },
  {
    scenario: '本架构·第5次迁移',
    M: 1,
    N: 0,
    C_linear: (1.2 * 1 + 1.5 * 0).toFixed(1),
    C_log: (Math.log(2) + Math.log(1)).toFixed(2),
    reduction: '↓ 94%',
    isNew: true
  },
  {
    scenario: '本架构·累计全迁移',
    M: 10,
    N: 0,
    C_linear: (1.2 * 10 + 1.5 * 0).toFixed(1),
    C_log: (Math.log(11) + Math.log(1)).toFixed(2),
    reduction: '↓ 40%',
    isNew: true
  }
]

// ─── 结论数据 ───────────────────────────────────────────────
const conclusions = [
  {
    title: '可扩展性显著优化',
    detail: '支持渐进式迁移，组件粒度解耦，迁移边界清晰，每次仅需迁移1个业务模块（M=1，N→0），复杂度降低94%以上。',
    icon: 'Promotion',
    iconColor: '#409eff',
    colorClass: 'con-blue',
    badge: '迁移复杂度 ↓94%',
    tagType: 'primary'
  },
  {
    title: '可伸缩性全面提升',
    detail: '支持任意业务模块独立横向扩容，哪个功能瓶颈就扩哪个，相比传统整体扩容资源利用率提升60%+。',
    icon: 'ScaleToOriginal',
    iconColor: '#67c23a',
    colorClass: 'con-green',
    badge: '资源利用率 ↑60%',
    tagType: 'success'
  },
  {
    title: '架构弹性显著增强',
    detail: '基础层与网关层提前构建并复用，不随业务变化重建，架构具备高弹性，满足渐进演化与业务快速迭代需求。',
    icon: 'Cpu',
    iconColor: '#e6a23c',
    colorClass: 'con-orange',
    badge: '弹性架构 高复用',
    tagType: 'warning'
  }
]

// ─── 图表引用 ────────────────────────────────────────────────
const complexityChartRef = ref(null)
const scalabilityChartRef = ref(null)
const extensibilityChartRef = ref(null)
let complexityChart, scalabilityChart, extensibilityChart

// ─── 迁移复杂度折线图 ─────────────────────────────────────────
const initComplexityChart = () => {
  complexityChart = echarts.init(complexityChartRef.value)
  const modules = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  // 传统架构：M = n（所有模块全量迁移），N = ceil(n/2)（新建组件约为模块数一半），α=1.2，β=1.5
  const traditional = modules.map(n => +(1.2 * n + 1.5 * Math.ceil(n / 2)).toFixed(1))
  // 本架构：每次只渐进迁移 M=1，N=0（网关/基础层已存在无需重建），累积复杂度 = n * α
  const newArch = modules.map(n => +(1.2 * n).toFixed(1))

  complexityChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
    legend: { data: ['传统架构（全拆全建）', '新型弹性架构（渐进迁移）'], top: 0, textStyle: { fontSize: 11 } },
    grid: { top: 40, left: 40, right: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: modules.map(n => `${n}模块`),
      name: '系统模块数量',
      nameLocation: 'end',
      nameTextStyle: { fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      name: '迁移复杂度C',
      nameTextStyle: { fontSize: 11 }
    },
    series: [
      {
        name: '传统架构（全拆全建）',
        type: 'line',
        data: traditional,
        smooth: true,
        lineStyle: { color: '#f56c6c', width: 2.5 },
        itemStyle: { color: '#f56c6c' },
        areaStyle: { color: 'rgba(245,108,108,0.08)' },
        symbol: 'circle',
        symbolSize: 6
      },
      {
        name: '新型弹性架构（渐进迁移）',
        type: 'line',
        data: newArch,
        smooth: true,
        lineStyle: { color: '#409eff', width: 2.5 },
        itemStyle: { color: '#409eff' },
        areaStyle: { color: 'rgba(64,158,255,0.08)' },
        symbol: 'circle',
        symbolSize: 6
      }
    ]
  })
}

// ─── 可伸缩性对比柱状图 ──────────────────────────────────────
const initScalabilityChart = () => {
  scalabilityChart = echarts.init(scalabilityChartRef.value)
  scalabilityChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['传统单体架构', '本新型弹性架构'], top: 0 },
    grid: { top: 40, left: 50, right: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: ['扩容粒度\n(越高越好)', '资源利用率\n(越高越好)', '故障隔离\n(越高越好)', '扩容响应\n(越快越好)', '弹性能力\n(越高越好)'],
      axisLabel: { fontSize: 10, interval: 0 }
    },
    yAxis: {
      type: 'value',
      max: 100,
      name: '评分 (0-100)',
      nameTextStyle: { fontSize: 11 }
    },
    series: [
      {
        name: '传统单体架构',
        type: 'bar',
        barWidth: '30%',
        data: [20, 30, 15, 25, 20],
        itemStyle: { color: '#f56c6c', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top', fontSize: 10 }
      },
      {
        name: '本新型弹性架构',
        type: 'bar',
        barWidth: '30%',
        data: [90, 85, 92, 88, 95],
        itemStyle: { color: '#67c23a', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top', fontSize: 10 }
      }
    ]
  })
}

// ─── 可扩展性渐进迁移瀑布图 ──────────────────────────────────
const initExtensibilityChart = () => {
  extensibilityChart = echarts.init(extensibilityChartRef.value)
  extensibilityChart.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['传统架构迁移成本', '本架构单次迁移成本', '本架构累计成本'], top: 0, textStyle: { fontSize: 11 } },
    grid: { top: 50, left: 50, right: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: ['第1次', '第2次', '第3次', '第4次', '第5次', '第6次', '第7次', '第8次', '第9次', '第10次'],
      name: '迁移批次',
      nameLocation: 'end',
      axisLabel: { fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      name: '复杂度成本',
      nameTextStyle: { fontSize: 11 }
    },
    series: [
      {
        name: '传统架构迁移成本',
        type: 'bar',
        barWidth: '25%',
        data: [19.5, 19.5, 19.5, 19.5, 19.5, 19.5, 19.5, 19.5, 19.5, 19.5],
        itemStyle: { color: '#f56c6c', borderRadius: [4, 4, 0, 0] }
      },
      {
        name: '本架构单次迁移成本',
        type: 'bar',
        barWidth: '25%',
        data: [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
        itemStyle: { color: '#409eff', borderRadius: [4, 4, 0, 0] }
      },
      {
        name: '本架构累计成本',
        type: 'line',
        data: [1.2, 2.4, 3.6, 4.8, 6.0, 7.2, 8.4, 9.6, 10.8, 12.0],
        smooth: true,
        lineStyle: { color: '#e6a23c', width: 2, type: 'dashed' },
        itemStyle: { color: '#e6a23c' },
        symbol: 'diamond',
        symbolSize: 7
      }
    ]
  })
}

// ─── 生命周期 ────────────────────────────────────────────────
onMounted(() => {
  initComplexityChart()
  initScalabilityChart()
  initExtensibilityChart()

  window.addEventListener('resize', handleResize)
})

const handleResize = () => {
  complexityChart?.resize()
  scalabilityChart?.resize()
  extensibilityChart?.resize()
}

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  complexityChart?.dispose()
  scalabilityChart?.dispose()
  extensibilityChart?.dispose()
})
</script>

<style scoped>
.arch-analysis {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ── 页面标题 ── */
.page-header-card {
  background: linear-gradient(135deg, #e8f4fd 0%, #f0f9eb 100%);
  border: 1px solid #b3d9f7;
}
.page-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}
.page-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a3a6e;
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.page-desc {
  color: #5a7aaa;
  font-size: 13px;
  line-height: 1.7;
  margin: 0;
}

/* ── 分区卡片通用 ── */
.section-card {
  height: 100%;
}
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.section-title {
  font-weight: 600;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* ── 架构形态卡片 ── */
.arch-card {
  border-radius: 12px;
  padding: 16px;
  border: 2px solid transparent;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.arch-monolith {
  background: #fff8f8;
  border-color: #fbc4c4;
}
.arch-middle {
  background: #fffbf0;
  border-color: #f5dab1;
}
.arch-micro {
  background: #f6ffed;
  border-color: #b7eb8f;
}

.arch-card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #ddd;
}
.arch-badge {
  background: #1a3a6e;
  color: #fff;
  font-size: 11px;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.arch-icon-wrap {
  width: 56px;
  height: 56px;
  background: rgba(255,255,255,0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.arch-title {
  font-size: 16px;
  font-weight: 700;
  color: #222;
}
.arch-subtitle {
  font-size: 11px;
  color: #888;
}

.arch-layers {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.arch-layer {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.layer-name {
  font-size: 12px;
  font-weight: 600;
  color: #333;
}
.layer-desc {
  font-size: 11px;
  color: #888;
}

.arch-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.metric {
  display: flex;
  align-items: center;
  gap: 8px;
}
.metric-label {
  font-size: 11px;
  color: #666;
  min-width: 70px;
  flex-shrink: 0;
}
.metric-val {
  font-size: 11px;
  font-weight: 600;
  min-width: 30px;
  text-align: right;
  flex-shrink: 0;
}
.arch-metrics :deep(.el-progress) {
  flex: 1;
}
.arch-metrics :deep(.el-progress-bar__outer) {
  border-radius: 4px;
}

.arch-pros-cons {
  font-size: 11px;
}
.pros, .cons {
  margin-bottom: 4px;
}
.pros ul, .cons ul {
  margin: 2px 0 0 16px;
  padding: 0;
}
.pros ul li, .cons ul li {
  color: #555;
  margin-bottom: 2px;
}
.pros-label {
  font-weight: 600;
  color: #67c23a;
}
.cons-label {
  font-weight: 600;
  color: #e6a23c;
}

/* ── 演化箭头 ── */
.evolution-arrow {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}
.arrow-label {
  font-size: 12px;
  color: #999;
}
.arrow-line {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}
.arrow-node {
  background: #f0f7ff;
  border: 1px solid #b3d0f7;
  color: #409eff;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}
.arrow-node.active {
  background: #f6ffed;
  border-color: #b7eb8f;
  color: #67c23a;
}
.arrow-sep {
  color: #aaa;
  font-size: 13px;
}

/* ── 公式区域 ── */
.formula-block {
  background: #f8faff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid #e0eaff;
}
.formula-title {
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 6px;
}
.mt-16 { margin-top: 16px; }
.formula-main {
  font-size: 22px;
  font-weight: 700;
  color: #1a3a6e;
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #fff;
  border-radius: 6px;
  display: inline-block;
  border: 1.5px solid #b3d0f7;
}
.formula-vars {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 4px;
}
.var-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
  font-size: 12px;
}
.var-name {
  font-weight: 700;
  color: #409eff;
  font-family: 'Courier New', monospace;
  min-width: 20px;
}
.var-desc {
  color: #555;
}
.formula-note {
  font-size: 11px;
  color: #888;
  margin-top: 6px;
  font-style: italic;
}

/* ── 对比表格 ── */
.compare-table-wrap {
  margin-top: 4px;
}
.compare-title {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}
.value-high {
  color: #f56c6c;
  font-weight: 700;
}
.value-low {
  color: #67c23a;
  font-weight: 700;
}

/* ── 图表 ── */
.chart-container {
  height: 260px;
}
.chart-legend {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 8px;
  font-size: 12px;
}
.legend-red { color: #f56c6c; }
.legend-blue { color: #409eff; }
.chart-section { display: flex; flex-direction: column; }

/* ── 可伸缩性说明 ── */
.scalability-desc {
  margin-top: 12px;
}

/* ── Steps ── */
.migration-steps {
  margin-top: 12px;
}
.migration-steps :deep(.el-step__title) {
  font-size: 12px;
}
.migration-steps :deep(.el-step__description) {
  font-size: 11px;
}

/* ── 结论区 ── */
.conclusion-card {
  background: linear-gradient(135deg, #f8faff 0%, #f6ffed 100%);
}
.conclusion-item {
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  height: 100%;
}
.con-blue { background: #e8f4fd; border: 1px solid #b3d9f7; }
.con-green { background: #f0f9eb; border: 1px solid #b7eb8f; }
.con-orange { background: #fdf6ec; border: 1px solid #f5dab1; }
.con-icon {
  width: 54px;
  height: 54px;
  background: rgba(255,255,255,0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.con-title {
  font-size: 15px;
  font-weight: 700;
  color: #222;
}
.con-detail {
  font-size: 12px;
  color: #555;
  line-height: 1.7;
}
.con-badge {
  margin-top: 4px;
}
</style>

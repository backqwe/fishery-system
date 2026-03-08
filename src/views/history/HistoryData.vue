<template>
  <div class="history-data">
    <!-- 搜索栏 -->
    <el-card shadow="never" class="search-card">
      <el-form inline :model="searchForm" label-width="80px">
        <el-form-item label="监测点">
          <el-select v-model="searchForm.pointId" placeholder="请选择监测点" clearable style="width:160px">
            <el-option v-for="p in pointOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width:260px"
          />
        </el-form-item>
        <el-form-item label="数据状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:120px">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="异常" value="异常" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
          <el-button type="success" @click="exportData"><el-icon><Download /></el-icon>导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Tab切换：表格模式 / 图表分析模式 -->
    <el-card shadow="never" class="content-card">
      <template #header>
        <div class="card-header">
          <span class="title">历史监测数据</span>
          <el-radio-group v-model="viewMode" size="small">
            <el-radio-button label="table">
              <el-icon><Grid /></el-icon> 表格模式
            </el-radio-button>
            <el-radio-button label="chart">
              <el-icon><TrendCharts /></el-icon> 图表分析
            </el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <!-- 表格模式 -->
      <div v-show="viewMode === 'table'">
        <el-table :data="pagedData" stripe border style="width:100%" size="small">
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="pointName" label="监测点" min-width="140" />
          <el-table-column prop="recordTime" label="记录时间" width="160" />
          <el-table-column prop="temperature" label="水温(°C)" width="90" align="center">
            <template #default="{ row }">
              <span :class="getClass(row.temperature, 18, 28)">{{ row.temperature }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="ph" label="pH值" width="80" align="center">
            <template #default="{ row }">
              <span :class="getClass(row.ph, 6.5, 8.5)">{{ row.ph }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="dissolvedOxygen" label="溶氧(mg/L)" width="100" align="center">
            <template #default="{ row }">
              <span :class="getClassMin(row.dissolvedOxygen, 5)">{{ row.dissolvedOxygen }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="ammoniaNitrogen" label="氨氮(mg/L)" width="100" align="center">
            <template #default="{ row }">
              <span :class="getClass(row.ammoniaNitrogen, 0, 0.3)">{{ row.ammoniaNitrogen }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="turbidity" label="浑浊度(NTU)" width="110" align="center" />
          <el-table-column prop="status" label="状态" width="80" align="center">
            <template #default="{ row }">
              <el-tag :type="row.status === '正常' ? 'success' : row.status === '预警' ? 'warning' : 'danger'" size="small">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-wrap">
          <el-pagination
            v-model:current-page="page"
            v-model:page-size="pageSize"
            :total="filteredData.length"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            background
          />
        </div>
      </div>

      <!-- 图表分析模式 -->
      <div v-show="viewMode === 'chart'">
        <el-row :gutter="16" class="chart-selector">
          <el-col :span="24">
            <el-radio-group v-model="chartMetric" @change="renderHistoryChart">
              <el-radio-button label="temperature">水温</el-radio-button>
              <el-radio-button label="ph">pH值</el-radio-button>
              <el-radio-button label="dissolvedOxygen">溶解氧</el-radio-button>
              <el-radio-button label="ammoniaNitrogen">氨氮</el-radio-button>
              <el-radio-button label="turbidity">浑浊度</el-radio-button>
            </el-radio-group>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :xs="24">
            <div ref="historyChartRef" style="height:360px;width:100%"></div>
          </el-col>
        </el-row>
        <el-row :gutter="16" style="margin-top:16px">
          <el-col :xs="24" :sm="8">
            <el-card class="stat-mini" shadow="hover">
              <div class="stat-mini-label">最大值</div>
              <div class="stat-mini-value" style="color:#f56c6c">{{ chartStats.max }}</div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="8">
            <el-card class="stat-mini" shadow="hover">
              <div class="stat-mini-label">最小值</div>
              <div class="stat-mini-value" style="color:#409eff">{{ chartStats.min }}</div>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="8">
            <el-card class="stat-mini" shadow="hover">
              <div class="stat-mini-label">平均值</div>
              <div class="stat-mini-value" style="color:#67c23a">{{ chartStats.avg }}</div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

// ===================== Mock 历史数据生成（约150条） =====================
const generateHistoryData = () => {
  const data = []
  const points = [
    { id: 1, name: 'A区-1号监测点' },
    { id: 2, name: 'A区-2号监测点' },
    { id: 3, name: 'B区-1号监测点' },
  ]
  const baseDate = new Date('2024-03-01')
  for (let d = 0; d < 6; d++) {
    for (let h = 0; h < 24; h += 2) {
      for (const pt of points) {
        const dt = new Date(baseDate.getTime() + d * 86400000 + h * 3600000)
        const dateStr = `${dt.getFullYear()}-${String(dt.getMonth()+1).padStart(2,'0')}-${String(dt.getDate()).padStart(2,'0')} ${String(dt.getHours()).padStart(2,'0')}:00:00`
        const temp = +(21 + Math.random() * 4).toFixed(1)
        const ph = +(6.8 + Math.random() * 1).toFixed(2)
        const do_ = +(6 + Math.random() * 4).toFixed(1)
        const nh3 = +(0.05 + Math.random() * 0.25).toFixed(3)
        const turb = +(15 + Math.random() * 40).toFixed(0)
        const status = do_ < 5 || nh3 > 0.3 ? (do_ < 3 || nh3 > 0.5 ? '异常' : '预警') : '正常'
        data.push({ id: data.length + 1, pointId: pt.id, pointName: pt.name, recordTime: dateStr, temperature: temp, ph, dissolvedOxygen: do_, ammoniaNitrogen: nh3, turbidity: +turb, status })
      }
    }
  }
  return data
}

const allData = ref(generateHistoryData())

const pointOptions = [
  { id: 1, name: 'A区-1号监测点' },
  { id: 2, name: 'A区-2号监测点' },
  { id: 3, name: 'B区-1号监测点' },
]

const searchForm = reactive({ pointId: '', dateRange: [], status: '' })
const viewMode = ref('table')
const chartMetric = ref('dissolvedOxygen')
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return allData.value.filter(row => {
    if (searchForm.pointId && row.pointId !== searchForm.pointId) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    if (searchForm.dateRange?.length === 2) {
      const [s, e] = searchForm.dateRange
      if (row.recordTime < s || row.recordTime > e + ' 23:59:59') return false
    }
    return true
  })
})

const pagedData = computed(() => {
  const start = (page.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.pointId = ''; searchForm.dateRange = []; searchForm.status = '' }
const exportData = () => ElMessage.info('数据导出（Mock，实际项目接入后端API）')

const getClass = (v, min, max) => {
  if (v < min || v > max) return 'val-error'
  if (v < min * 1.1 || v > max * 0.95) return 'val-warn'
  return ''
}
const getClassMin = (v, min) => v < min ? 'val-error' : v < min + 1 ? 'val-warn' : ''

// 图表
const historyChartRef = ref(null)
let historyChart = null

const metricConfig = {
  temperature: { label: '水温(°C)', color: '#ff7043', unit: '°C', warnMin: 18, warnMax: 28 },
  ph: { label: 'pH值', color: '#5c6bc0', unit: '', warnMin: 6.5, warnMax: 8.5 },
  dissolvedOxygen: { label: '溶解氧(mg/L)', color: '#26a69a', unit: 'mg/L', warnMin: 5, warnMax: 12 },
  ammoniaNitrogen: { label: '氨氮(mg/L)', color: '#ab47bc', unit: 'mg/L', warnMin: 0, warnMax: 0.3 },
  turbidity: { label: '浑浊度(NTU)', color: '#8d6e63', unit: 'NTU', warnMin: 0, warnMax: 40 }
}

const chartStats = computed(() => {
  const metric = chartMetric.value
  const vals = filteredData.value.slice(0, 72).map(d => d[metric]).filter(v => v !== undefined)
  if (!vals.length) return { max: '-', min: '-', avg: '-' }
  const max = Math.max(...vals).toFixed(2)
  const min = Math.min(...vals).toFixed(2)
  const avg = (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(2)
  return { max, min, avg }
})

const renderHistoryChart = () => {
  if (!historyChart) return
  const metric = chartMetric.value
  const cfg = metricConfig[metric]
  // 取前72条数据展示
  const displayData = filteredData.value.slice(0, 72)
  const times = displayData.map(d => d.recordTime.slice(5, 16))
  const vals = displayData.map(d => d[metric])

  historyChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: [cfg.label], top: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
    dataZoom: [{ type: 'slider', bottom: 0 }, { type: 'inside' }],
    xAxis: { type: 'category', data: times, axisLabel: { rotate: 30, fontSize: 10 } },
    yAxis: { type: 'value', name: cfg.unit },
    series: [{
      name: cfg.label,
      type: 'line',
      data: vals,
      smooth: true,
      lineStyle: { color: cfg.color, width: 2 },
      itemStyle: { color: cfg.color },
      areaStyle: {
        color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [{ offset: 0, color: cfg.color + '30' }, { offset: 1, color: cfg.color + '05' }]
        }
      },
      markLine: {
        silent: true,
        lineStyle: { color: '#f56c6c', type: 'dashed' },
        data: [
          { yAxis: cfg.warnMin, label: { formatter: '下限 {c}' } },
          { yAxis: cfg.warnMax, label: { formatter: '上限 {c}' } }
        ]
      }
    }]
  })
}

onMounted(() => {
  historyChart = echarts.init(historyChartRef.value)
  renderHistoryChart()
  window.addEventListener('resize', () => historyChart?.resize())
})

watch(viewMode, (val) => {
  if (val === 'chart') {
    setTimeout(() => {
      historyChart?.resize()
      renderHistoryChart()
    }, 100)
  }
})
</script>

<style scoped>
.history-data { display: flex; flex-direction: column; gap: 16px; }
.search-card {}
.content-card {}
.card-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.title { font-size: 16px; font-weight: 600; }
.chart-selector { margin-bottom: 16px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
.stat-mini { text-align: center; }
.stat-mini-label { font-size: 13px; color: #666; }
.stat-mini-value { font-size: 28px; font-weight: 700; margin-top: 4px; }
.val-warn { color: #e6a23c; font-weight: 600; }
.val-error { color: #f56c6c; font-weight: 700; }
</style>

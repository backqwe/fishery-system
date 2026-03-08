<template>
  <div class="realtime-monitor">
    <!-- 顶部搜索工具栏 -->
    <el-card shadow="never" class="search-bar">
      <el-form :model="searchForm" inline>
        <el-form-item label="养殖场">
          <el-select v-model="searchForm.farm" placeholder="全部养殖场" clearable style="width:140px">
            <el-option v-for="f in farmOptions" :key="f" :label="f" :value="f" />
          </el-select>
        </el-form-item>
        <el-form-item label="监测点">
          <el-select v-model="searchForm.point" placeholder="全部监测点" clearable style="width:160px">
            <el-option v-for="p in pointOptions" :key="p.value" :label="p.label" :value="p.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width:120px">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="异常" value="异常" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>查询</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
        <el-form-item style="float:right">
          <el-tag type="success" class="update-time">
            <el-icon class="is-loading"><Loading /></el-icon>
            实时更新中 &nbsp;{{ currentTime }}
          </el-tag>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 数据统计卡片 -->
    <el-row :gutter="16" class="stat-cards">
      <el-col :xs="12" :sm="6" v-for="card in statCards" :key="card.key">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-card-inner">
            <div class="stat-icon-wrap" :style="{ background: card.gradient }">
              <el-icon size="28" color="#fff"><component :is="card.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-num">
                <span class="stat-value" :class="card.valueClass">{{ card.value }}</span>
                <span class="stat-unit">{{ card.unit }}</span>
              </div>
              <div class="stat-label">{{ card.label }}</div>
            </div>
            <div class="stat-trend" :class="card.trendClass">
              <el-icon size="12"><component :is="card.trendIcon" /></el-icon>
              {{ card.trendText }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="16" class="charts-row">
      <!-- 实时水质折线图 -->
      <el-col :xs="24" :lg="16">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span class="chart-title">
                <el-icon color="#409eff"><DataAnalysis /></el-icon>
                实时水质指标监测（近30分钟）
              </span>
              <el-radio-group v-model="selectedMetric" size="small" @change="renderRealtimeChart">
                <el-radio-button label="temperature">水温</el-radio-button>
                <el-radio-button label="ph">pH值</el-radio-button>
                <el-radio-button label="dissolvedOxygen">溶氧量</el-radio-button>
                <el-radio-button label="ammoniaNitrogen">氨氮</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="realtimeChartRef" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 各监测点当前状态 -->
      <el-col :xs="24" :lg="8">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="chart-header">
              <span class="chart-title">
                <el-icon color="#67c23a"><LocationInformation /></el-icon>
                监测点状态分布
              </span>
            </div>
          </template>
          <div ref="statusChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 监测数据表格 + 报警列表 -->
    <el-row :gutter="16" class="bottom-row">
      <!-- 当前监测数据表格 -->
      <el-col :xs="24" :lg="14">
        <el-card shadow="hover">
          <template #header>
            <div class="chart-header">
              <span class="chart-title">
                <el-icon color="#e6a23c"><Monitor /></el-icon>
                当前监测数据
              </span>
              <el-button type="primary" link size="small" @click="exportData">
                <el-icon><Download /></el-icon>导出
              </el-button>
            </div>
          </template>
          <el-table :data="filteredMonitorData" stripe size="small" style="width:100%">
            <el-table-column prop="pointName" label="监测点" min-width="110" />
            <el-table-column prop="temperature" label="水温(°C)" width="90" align="center">
              <template #default="{ row }">
                <span :class="getValueClass(row.temperature, 15, 30)">{{ row.temperature }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="ph" label="pH" width="75" align="center">
              <template #default="{ row }">
                <span :class="getValueClass(row.ph, 6.5, 8.5)">{{ row.ph }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="dissolvedOxygen" label="溶氧(mg/L)" width="100" align="center">
              <template #default="{ row }">
                <span :class="getValueClass(row.dissolvedOxygen, 5, 12, true)">{{ row.dissolvedOxygen }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="ammoniaNitrogen" label="氨氮(mg/L)" width="100" align="center">
              <template #default="{ row }">
                <span :class="getValueClass(row.ammoniaNitrogen, 0, 0.3)">{{ row.ammoniaNitrogen }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="80" align="center">
              <template #default="{ row }">
                <el-tag :type="row.status === '正常' ? 'success' : row.status === '预警' ? 'warning' : 'danger'" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="updateTime" label="更新时间" min-width="130" />
          </el-table>
        </el-card>
      </el-col>

      <!-- 实时报警列表 -->
      <el-col :xs="24" :lg="10">
        <el-card shadow="hover" class="alarm-card">
          <template #header>
            <div class="chart-header">
              <span class="chart-title">
                <el-icon color="#f56c6c"><Warning /></el-icon>
                实时报警列表
                <el-badge :value="alarmList.filter(a=>!a.handled).length" class="alarm-badge" />
              </span>
              <el-button type="danger" link size="small" @click="handleAllAlarms">一键处理</el-button>
            </div>
          </template>
          <div class="alarm-list">
            <div
              v-for="alarm in alarmList"
              :key="alarm.id"
              class="alarm-item"
              :class="[`alarm-${alarm.level}`, { handled: alarm.handled }]"
            >
              <div class="alarm-dot" :class="`dot-${alarm.level}`"></div>
              <div class="alarm-content">
                <div class="alarm-title">
                  <span class="alarm-point">{{ alarm.point }}</span>
                  <el-tag :type="alarm.level === 'error' ? 'danger' : alarm.level === 'warning' ? 'warning' : 'info'" size="small">
                    {{ alarm.type }}
                  </el-tag>
                  <el-tag v-if="alarm.handled" type="info" size="small">已处理</el-tag>
                </div>
                <div class="alarm-desc">{{ alarm.content }}</div>
                <div class="alarm-time">{{ alarm.time }}</div>
              </div>
              <el-button
                v-if="!alarm.handled"
                type="primary"
                link
                size="small"
                @click="handleAlarm(alarm)"
              >处理</el-button>
            </div>
            <el-empty v-if="alarmList.length === 0" description="暂无报警信息" :image-size="60" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

// =============== Mock 数据（实际项目替换为API请求）================

// 监测点实时数据 Mock
const monitorData = ref([
  { id: 1, pointName: 'A区-1号监测点', pondName: '1号池塘', temperature: 22.5, ph: 7.2, dissolvedOxygen: 8.5, ammoniaNitrogen: 0.08, turbidity: 25, updateTime: '15:30:00', status: '正常' },
  { id: 2, pointName: 'A区-2号监测点', pondName: '2号池塘', temperature: 23.1, ph: 7.5, dissolvedOxygen: 9.0, ammoniaNitrogen: 0.06, turbidity: 22, updateTime: '15:30:00', status: '正常' },
  { id: 3, pointName: 'B区-1号监测点', pondName: '3号池塘', temperature: 24.8, ph: 6.8, dissolvedOxygen: 5.2, ammoniaNitrogen: 0.35, turbidity: 45, updateTime: '15:30:00', status: '预警' },
  { id: 4, pointName: 'B区-2号监测点', pondName: '4号池塘', temperature: 21.9, ph: 7.3, dissolvedOxygen: 8.8, ammoniaNitrogen: 0.07, turbidity: 20, updateTime: '15:30:00', status: '正常' },
  { id: 5, pointName: 'C区-1号监测点', pondName: '5号池塘', temperature: 22.3, ph: 7.1, dissolvedOxygen: 8.2, ammoniaNitrogen: 0.09, turbidity: 28, updateTime: '15:30:00', status: '正常' },
  { id: 6, pointName: 'C区-2号监测点', pondName: '6号池塘', temperature: 23.5, ph: 7.6, dissolvedOxygen: 9.2, ammoniaNitrogen: 0.05, turbidity: 18, updateTime: '15:30:00', status: '正常' },
  { id: 7, pointName: 'D区-1号监测点', pondName: '7号池塘', temperature: 25.2, ph: 6.5, dissolvedOxygen: 4.8, ammoniaNitrogen: 0.42, turbidity: 52, updateTime: '15:30:00', status: '异常' },
])

// 报警列表 Mock
const alarmList = ref([
  { id: 1, time: '2024-03-06 15:28', point: 'D区-1号监测点', type: '溶氧预警', content: '溶氧量严重偏低(4.8mg/L)，低于报警阈值5.0mg/L', level: 'error', handled: false },
  { id: 2, time: '2024-03-06 15:15', point: 'B区-1号监测点', type: '氨氮预警', content: '氨氮超标(0.35mg/L)，超过报警阈值0.3mg/L', level: 'error', handled: false },
  { id: 3, time: '2024-03-06 14:40', point: 'B区-1号监测点', type: 'pH预警', content: 'pH偏低(6.8)，低于正常范围6.9', level: 'warning', handled: false },
  { id: 4, time: '2024-03-06 13:10', point: 'A区-2号监测点', type: '浑浊度预警', content: '浑浊度偏高(45NTU)，超过阈值40NTU', level: 'warning', handled: true },
  { id: 5, time: '2024-03-06 11:30', point: '全部监测点', type: '设备提醒', content: 'D区增氧机运行时间超过8小时，建议检查', level: 'info', handled: true },
])

// 统计卡片数据 Mock
const statCards = ref([
  { key: 'total', label: '在线监测点', value: 18, unit: '个', icon: 'Monitor', gradient: 'linear-gradient(135deg,#1565c0,#0288d1)', trendClass: 'trend-up', trendIcon: 'ArrowUp', trendText: '全部在线' },
  { key: 'normal', label: '正常数量', value: 15, unit: '个', icon: 'CircleCheck', gradient: 'linear-gradient(135deg,#2e7d32,#43a047)', trendClass: 'trend-up', trendIcon: 'ArrowUp', trendText: '较昨日+1' },
  { key: 'warning', label: '预警数量', value: 2, unit: '个', icon: 'Warning', gradient: 'linear-gradient(135deg,#f57c00,#ff9800)', trendClass: 'trend-down', trendIcon: 'ArrowDown', trendText: '较昨日-1', valueClass: 'value-warning' },
  { key: 'error', label: '异常数量', value: 1, unit: '个', icon: 'CircleClose', gradient: 'linear-gradient(135deg,#c62828,#e53935)', trendClass: 'trend-down', trendIcon: 'ArrowUp', trendText: '需立即处理', valueClass: 'value-error' },
])

// 实时图表时间轴数据 Mock（近30分钟，每2分钟一个点）
const generateTimeAxis = () => {
  const now = new Date()
  const times = []
  for (let i = 14; i >= 0; i--) {
    const t = new Date(now.getTime() - i * 2 * 60000)
    times.push(`${String(t.getHours()).padStart(2,'0')}:${String(t.getMinutes()).padStart(2,'0')}`)
  }
  return times
}

// 各指标时序数据 Mock
const metricSeriesData = {
  temperature: {
    label: '水温(°C)',
    color: '#ff7043',
    data: [22.1, 22.3, 22.2, 22.5, 22.8, 23.0, 22.9, 22.7, 22.5, 22.6, 22.8, 23.1, 23.0, 22.9, 22.5],
    warningMin: 18,
    warningMax: 28,
    yMin: 15,
    yMax: 35
  },
  ph: {
    label: 'pH值',
    color: '#5c6bc0',
    data: [7.1, 7.2, 7.2, 7.3, 7.2, 7.1, 7.2, 7.3, 7.2, 7.1, 7.0, 6.9, 6.8, 6.9, 7.0],
    warningMin: 6.5,
    warningMax: 8.5,
    yMin: 5.5,
    yMax: 9.5
  },
  dissolvedOxygen: {
    label: '溶氧量(mg/L)',
    color: '#26a69a',
    data: [8.8, 8.6, 8.5, 8.7, 8.9, 9.0, 8.8, 8.5, 8.2, 7.8, 7.2, 6.5, 5.8, 5.2, 4.8],
    warningMin: 5.0,
    warningMax: 12.0,
    yMin: 2,
    yMax: 14
  },
  ammoniaNitrogen: {
    label: '氨氮(mg/L)',
    color: '#ab47bc',
    data: [0.08, 0.09, 0.08, 0.10, 0.11, 0.12, 0.14, 0.18, 0.22, 0.25, 0.28, 0.31, 0.33, 0.36, 0.42],
    warningMin: 0,
    warningMax: 0.3,
    yMin: 0,
    yMax: 0.6
  }
}

// 搜索表单
const searchForm = reactive({ farm: '', point: '', status: '' })
const farmOptions = ['第一养殖场', '第二养殖场', '第三养殖场']
const pointOptions = [
  { label: 'A区-1号监测点', value: 1 },
  { label: 'A区-2号监测点', value: 2 },
  { label: 'B区-1号监测点', value: 3 },
  { label: 'B区-2号监测点', value: 4 },
  { label: 'C区-1号监测点', value: 5 },
  { label: 'C区-2号监测点', value: 6 },
  { label: 'D区-1号监测点', value: 7 },
]

const filteredMonitorData = computed(() => {
  return monitorData.value.filter(item => {
    if (searchForm.status && item.status !== searchForm.status) return false
    if (searchForm.point && item.id !== searchForm.point) return false
    return true
  })
})

const handleSearch = () => { /* 实际项目中触发API查询 */ }
const resetSearch = () => { searchForm.farm = ''; searchForm.point = ''; searchForm.status = '' }

// =============== 图表 ================
const realtimeChartRef = ref(null)
const statusChartRef = ref(null)
let realtimeChart = null
let statusChart = null
const selectedMetric = ref('dissolvedOxygen')
const currentTime = ref('')

const getValueClass = (val, min, max, isMinCritical = false) => {
  if (isMinCritical) {
    if (val < min) return 'value-error'
    if (val < min + 1) return 'value-warning'
    return 'value-normal'
  }
  if (val < min || val > max) return 'value-error'
  if (val < min * 1.1 || val > max * 0.9) return 'value-warning'
  return 'value-normal'
}

const renderRealtimeChart = () => {
  if (!realtimeChart) return
  const metric = metricSeriesData[selectedMetric.value]
  const times = generateTimeAxis()

  realtimeChart.setOption({
    tooltip: { trigger: 'axis', formatter: (params) => `${params[0].axisValue}<br/>${metric.label}: <b>${params[0].value}</b>` },
    grid: { left: '3%', right: '4%', bottom: '12%', top: '15%', containLabel: true },
    xAxis: { type: 'category', data: times, axisLabel: { fontSize: 11 } },
    yAxis: {
      type: 'value',
      min: metric.yMin,
      max: metric.yMax,
      axisLabel: { fontSize: 11 }
    },
    series: [
      {
        name: metric.label,
        type: 'line',
        data: metric.data,
        smooth: true,
        lineStyle: { color: metric.color, width: 2.5 },
        itemStyle: { color: metric.color },
        areaStyle: {
          color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: metric.color + '40' },
              { offset: 1, color: metric.color + '05' }
            ]
          }
        },
        markLine: {
          silent: true,
          lineStyle: { color: '#f56c6c', type: 'dashed' },
          data: [
            { yAxis: metric.warningMin, name: '下限', label: { formatter: '下限 {c}' } },
            { yAxis: metric.warningMax, name: '上限', label: { formatter: '上限 {c}' } }
          ]
        }
      }
    ]
  })
}

const renderStatusChart = () => {
  if (!statusChart) return
  // Mock 状态分布数据
  statusChart.setOption({
    tooltip: { trigger: 'item', formatter: '{a}<br/>{b}: {c} ({d}%)' },
    legend: { bottom: 0, data: ['正常', '预警', '异常', '离线'] },
    series: [{
      name: '监测点状态',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: false,
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false, position: 'center' },
      emphasis: {
        label: { show: true, fontSize: 16, fontWeight: 'bold' }
      },
      data: [
        { value: 15, name: '正常', itemStyle: { color: '#67c23a' } },
        { value: 2, name: '预警', itemStyle: { color: '#e6a23c' } },
        { value: 1, name: '异常', itemStyle: { color: '#f56c6c' } },
        { value: 0, name: '离线', itemStyle: { color: '#909399' } }
      ]
    }]
  })
}

// 模拟实时数据更新
let updateTimer = null
const updateCurrentTime = () => {
  const now = new Date()
  currentTime.value = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}`
}

const simulateDataUpdate = () => {
  // 模拟数据微小波动
  monitorData.value = monitorData.value.map(item => ({
    ...item,
    temperature: +(item.temperature + (Math.random() - 0.5) * 0.2).toFixed(1),
    ph: +(item.ph + (Math.random() - 0.5) * 0.05).toFixed(2),
    dissolvedOxygen: +(item.dissolvedOxygen + (Math.random() - 0.5) * 0.3).toFixed(1),
    ammoniaNitrogen: +(item.ammoniaNitrogen + (Math.random() - 0.5) * 0.02).toFixed(2),
    updateTime: currentTime.value
  }))
}

const handleAlarm = (alarm) => {
  alarm.handled = true
  ElMessage.success(`报警 "${alarm.type}" 已标记处理`)
}

const handleAllAlarms = () => {
  alarmList.value.forEach(a => { a.handled = true })
  ElMessage.success('已一键处理全部报警')
}

const exportData = () => {
  ElMessage.info('数据导出功能（Mock，实际项目接入后端API）')
}

onMounted(() => {
  realtimeChart = echarts.init(realtimeChartRef.value)
  statusChart = echarts.init(statusChartRef.value)
  renderRealtimeChart()
  renderStatusChart()
  updateCurrentTime()
  updateTimer = setInterval(() => {
    updateCurrentTime()
    simulateDataUpdate()
    renderRealtimeChart()
  }, 5000)

  window.addEventListener('resize', () => {
    realtimeChart?.resize()
    statusChart?.resize()
  })
})

onUnmounted(() => {
  clearInterval(updateTimer)
  realtimeChart?.dispose()
  statusChart?.dispose()
})
</script>

<style scoped>
.realtime-monitor { display: flex; flex-direction: column; gap: 16px; }

.search-bar :deep(.el-form) { flex-wrap: wrap; }
.update-time { font-size: 13px; }

.stat-cards { margin: 0; }
.stat-card { border-radius: 10px; overflow: hidden; transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-3px); }
.stat-card-inner {
  display: flex;
  align-items: center;
  gap: 14px;
  position: relative;
}
.stat-icon-wrap {
  width: 52px; height: 52px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.stat-info { flex: 1; }
.stat-num { display: flex; align-items: baseline; gap: 4px; }
.stat-value { font-size: 28px; font-weight: 700; color: #1a2a4a; }
.stat-value.value-warning { color: #e6a23c; }
.stat-value.value-error { color: #f56c6c; }
.stat-unit { font-size: 13px; color: #888; }
.stat-label { font-size: 13px; color: #666; margin-top: 2px; }
.stat-trend { position: absolute; top: 0; right: 0; font-size: 11px; display: flex; align-items: center; gap: 2px; }
.trend-up { color: #67c23a; }
.trend-down { color: #f56c6c; }

.chart-card { border-radius: 10px; }
.chart-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.chart-title { display: flex; align-items: center; gap: 6px; font-weight: 600; font-size: 14px; }

.chart-container { height: 280px; }

.alarm-card .alarm-list { max-height: 330px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
.alarm-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  background: #fff8f8; border-left: 3px solid #f56c6c;
  transition: all 0.2s;
}
.alarm-item.alarm-warning { background: #fffbf0; border-left-color: #e6a23c; }
.alarm-item.alarm-info { background: #f0f9ff; border-left-color: #409eff; }
.alarm-item.handled { opacity: 0.5; background: #f9f9f9; border-left-color: #ddd; }

.alarm-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 6px; }
.dot-error { background: #f56c6c; box-shadow: 0 0 0 3px rgba(245,108,108,0.3); }
.dot-warning { background: #e6a23c; box-shadow: 0 0 0 3px rgba(230,162,60,0.3); }
.dot-info { background: #409eff; box-shadow: 0 0 0 3px rgba(64,158,255,0.3); }

.alarm-content { flex: 1; min-width: 0; }
.alarm-title { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-bottom: 4px; }
.alarm-point { font-size: 13px; font-weight: 600; color: #303133; }
.alarm-desc { font-size: 12px; color: #606266; line-height: 1.5; }
.alarm-time { font-size: 11px; color: #aaa; margin-top: 3px; }
.alarm-badge { margin-left: 6px; }

.value-normal { color: #67c23a; }
.value-warning { color: #e6a23c; font-weight: 600; }
.value-error { color: #f56c6c; font-weight: 700; }

.bottom-row { margin-top: 0; }
.charts-row { margin-top: 0; }
</style>

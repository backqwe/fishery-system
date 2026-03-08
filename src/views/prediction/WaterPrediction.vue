<template>
  <div class="water-prediction">
    <!-- 搜索与参数配置 -->
    <el-card shadow="never" class="param-card">
      <el-form inline :model="paramForm">
        <el-form-item label="监测点">
          <el-select v-model="paramForm.pointId" placeholder="请选择监测点" style="width:160px" @change="refreshChart">
            <el-option v-for="p in pointOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="预测指标">
          <el-select v-model="paramForm.metric" placeholder="选择指标" style="width:140px" @change="refreshChart">
            <el-option v-for="m in metricOptions" :key="m.value" :label="m.label" :value="m.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="预测模型">
          <el-select v-model="paramForm.model" placeholder="选择模型" style="width:160px" @change="refreshChart">
            <el-option label="LSTM神经网络" value="LSTM" />
            <el-option label="ARIMA时序模型" value="ARIMA" />
            <el-option label="Prophet模型" value="Prophet" />
          </el-select>
        </el-form-item>
        <el-form-item label="预测时长">
          <el-select v-model="paramForm.hours" style="width:120px" @change="refreshChart">
            <el-option label="未来6小时" :value="6" />
            <el-option label="未来12小时" :value="12" />
            <el-option label="未来24小时" :value="24" />
            <el-option label="未来48小时" :value="48" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="refreshChart">
            <el-icon><Refresh /></el-icon>重新预测
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 模型指标卡片 -->
    <el-row :gutter="16">
      <el-col :xs="12" :sm="6" v-for="kpi in modelKpis" :key="kpi.key">
        <el-card class="kpi-card" shadow="hover">
          <div class="kpi-inner">
            <div class="kpi-label">{{ kpi.label }}</div>
            <div class="kpi-value" :style="{ color: kpi.color }">{{ kpi.value }}</div>
            <div class="kpi-desc">{{ kpi.desc }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预测折线图 -->
    <el-card shadow="hover" class="chart-card">
      <template #header>
        <div class="chart-header">
          <span class="chart-title">
            <el-icon color="#409eff"><TrendCharts /></el-icon>
            {{ currentMetricLabel }} 实际值与预测值对比
            <el-tag size="small" type="info" style="margin-left:8px">{{ paramForm.model }} 模型</el-tag>
          </span>
          <div style="display:flex;gap:12px;align-items:center">
            <span class="legend-item"><span class="legend-dot" style="background:#409eff"></span>历史实际值</span>
            <span class="legend-item"><span class="legend-dot" style="background:#f56c6c;border-style:dashed"></span>预测值</span>
            <span class="legend-item"><span class="legend-dot" style="background:#e6a23c;opacity:0.3"></span>置信区间</span>
          </div>
        </div>
      </template>
      <div ref="predictionChartRef" class="chart-container"></div>
    </el-card>

    <!-- 预测数据表格 -->
    <el-card shadow="hover">
      <template #header>
        <div class="chart-header">
          <span class="chart-title">
            <el-icon color="#67c23a"><Calendar /></el-icon>
            预测数据详情（未来 {{ paramForm.hours }} 小时）
          </span>
        </div>
      </template>
      <el-table :data="predictionTableData" stripe border size="small" style="width:100%">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="time" label="预测时间" width="160" />
        <el-table-column prop="predicted" :label="`预测${currentMetricLabel}`" width="140" align="center">
          <template #default="{ row }">
            <span class="pred-value">{{ row.predicted }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="lower" label="置信下界" width="120" align="center">
          <template #default="{ row }">
            <span style="color:#909399">{{ row.lower }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="upper" label="置信上界" width="120" align="center">
          <template #default="{ row }">
            <span style="color:#909399">{{ row.upper }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="risk" label="风险评估" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.risk === '正常' ? 'success' : row.risk === '预警' ? 'warning' : 'danger'" size="small">
              {{ row.risk }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="suggestion" label="处理建议" min-width="200" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// ===================== Mock 数据配置 =====================
const pointOptions = [
  { id: 1, name: 'A区-1号监测点' },
  { id: 2, name: 'A区-2号监测点' },
  { id: 3, name: 'B区-1号监测点' },
]

const metricOptions = [
  { label: '溶解氧(mg/L)', value: 'dissolvedOxygen' },
  { label: '水温(°C)', value: 'temperature' },
  { label: 'pH值', value: 'ph' },
  { label: '氨氮(mg/L)', value: 'ammoniaNitrogen' },
]

const paramForm = reactive({ pointId: 1, metric: 'dissolvedOxygen', model: 'LSTM', hours: 24 })

// 模型性能指标 Mock
const modelKpis = ref([
  { key: 'mae', label: '平均绝对误差(MAE)', value: '0.183', color: '#409eff', desc: '越小越好' },
  { key: 'rmse', label: '均方根误差(RMSE)', value: '0.241', color: '#67c23a', desc: '越小越好' },
  { key: 'r2', label: '决定系数(R²)', value: '0.956', color: '#e6a23c', desc: '越接近1越好' },
  { key: 'acc', label: '预测准确率', value: '94.8%', color: '#f56c6c', desc: '阈值判断准确率' },
])

const currentMetricLabel = computed(() => {
  return metricOptions.find(m => m.value === paramForm.metric)?.label?.split('(')[0] || ''
})

// 生成历史数据与预测数据 Mock
const generateData = (metric, hours) => {
  const now = new Date('2024-03-06T15:00:00')
  const histTimes = []
  const histVals = []
  const predTimes = []
  const predVals = []
  const predLower = []
  const predUpper = []

  const baseMap = {
    dissolvedOxygen: { base: 8.5, range: 1.5, min: 3, max: 14, warnMin: 5, warnMax: 12, unit: 'mg/L' },
    temperature: { base: 23, range: 2, min: 10, max: 40, warnMin: 18, warnMax: 28, unit: '°C' },
    ph: { base: 7.2, range: 0.4, min: 5, max: 10, warnMin: 6.5, warnMax: 8.5, unit: '' },
    ammoniaNitrogen: { base: 0.12, range: 0.08, min: 0, max: 1, warnMin: 0, warnMax: 0.3, unit: 'mg/L' },
  }
  const cfg = baseMap[metric] || baseMap.dissolvedOxygen

  // 历史数据 (过去24小时)
  for (let i = -24; i <= 0; i++) {
    const t = new Date(now.getTime() + i * 3600000)
    histTimes.push(`${String(t.getMonth()+1).padStart(2,'0')}-${String(t.getDate()).padStart(2,'0')} ${String(t.getHours()).padStart(2,'0')}:00`)
    // 模拟趋势：溶氧量在下午到夜间下降
    const trend = metric === 'dissolvedOxygen' ? -0.05 * i : (metric === 'ammoniaNitrogen' ? 0.003 * i : 0)
    const val = +(cfg.base + (Math.sin(i * 0.3) * cfg.range * 0.6) + (Math.random() - 0.5) * cfg.range * 0.4 + trend).toFixed(3)
    histVals.push(Math.max(cfg.min, Math.min(cfg.max, val)))
  }

  // 预测数据
  const lastHistVal = histVals[histVals.length - 1]
  for (let i = 1; i <= hours; i++) {
    const t = new Date(now.getTime() + i * 3600000)
    predTimes.push(`${String(t.getMonth()+1).padStart(2,'0')}-${String(t.getDate()).padStart(2,'0')} ${String(t.getHours()).padStart(2,'0')}:00`)
    // 预测值：带一定衰减趋势的随机波动
    const trend = metric === 'dissolvedOxygen' ? -0.08 * i : (metric === 'ammoniaNitrogen' ? 0.005 * i : 0)
    const predicted = +(lastHistVal + trend + (Math.sin(i * 0.5) * cfg.range * 0.5) + (Math.random() - 0.5) * cfg.range * 0.3).toFixed(3)
    const pVal = Math.max(cfg.min, Math.min(cfg.max, predicted))
    const conf = cfg.range * 0.1 * Math.sqrt(i)
    predVals.push(pVal)
    predLower.push(+(pVal - conf).toFixed(3))
    predUpper.push(+(pVal + conf).toFixed(3))
  }

  return { histTimes, histVals, predTimes, predVals, predLower, predUpper, cfg }
}

const predictionTableData = computed(() => {
  const cfg = baseMap[paramForm.metric] || baseMap.dissolvedOxygen
  const { predTimes, predVals, predLower, predUpper } = generateData(paramForm.metric, paramForm.hours)
  return predTimes.map((time, i) => {
    const pv = predVals[i]
    let risk = '正常', suggestion = '水质状况良好，保持正常养殖管理'
    if (paramForm.metric === 'dissolvedOxygen') {
      if (pv < 3) { risk = '异常'; suggestion = '溶氧严重不足，立即开启所有增氧设备，减少饲料投喂量' }
      else if (pv < 5) { risk = '预警'; suggestion = '溶氧偏低，请增大增氧力度，关注鱼群状态' }
    } else if (paramForm.metric === 'ammoniaNitrogen') {
      if (pv > 0.5) { risk = '异常'; suggestion = '氨氮严重超标，立即换水，使用水质改良剂' }
      else if (pv > 0.3) { risk = '预警'; suggestion = '氨氮偏高，适量换水，减少投喂' }
    }
    return { time, predicted: pv.toFixed(3), lower: predLower[i], upper: predUpper[i], risk, suggestion }
  })
})

const baseMap = {
  dissolvedOxygen: { base: 8.5, range: 1.5, min: 3, max: 14, warnMin: 5, warnMax: 12, unit: 'mg/L' },
  temperature: { base: 23, range: 2, min: 10, max: 40, warnMin: 18, warnMax: 28, unit: '°C' },
  ph: { base: 7.2, range: 0.4, min: 5, max: 10, warnMin: 6.5, warnMax: 8.5, unit: '' },
  ammoniaNitrogen: { base: 0.12, range: 0.08, min: 0, max: 1, warnMin: 0, warnMax: 0.3, unit: 'mg/L' },
}

// 图表
const predictionChartRef = ref(null)
let predChart = null

const refreshChart = () => {
  if (!predChart) return
  const { histTimes, histVals, predTimes, predVals, predLower, predUpper, cfg } = generateData(paramForm.metric, paramForm.hours)
  const allTimes = [...histTimes, ...predTimes]
  const histPad = new Array(histVals.length).fill(null)
  const predPad = new Array(histVals.length - 1).fill(null)

  // 拼接历史与预测（预测起点与历史末尾重叠）
  const predValFull = [...predPad, histVals[histVals.length - 1], ...predVals]
  const lowerFull = [...predPad, histVals[histVals.length - 1], ...predLower]
  const upperFull = [...predPad, histVals[histVals.length - 1], ...predUpper]

  predChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['历史实际值', '预测值'], top: 0 },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '12%', containLabel: true },
    dataZoom: [{ type: 'slider', bottom: 0 }, { type: 'inside' }],
    xAxis: { type: 'category', data: allTimes, axisLabel: { rotate: 30, fontSize: 10 }, boundaryGap: false },
    yAxis: { type: 'value', name: cfg.unit || '' },
    series: [
      {
        name: '历史实际值',
        type: 'line',
        data: [...histVals, ...new Array(predTimes.length).fill(null)],
        smooth: false,
        lineStyle: { color: '#409eff', width: 2.5 },
        itemStyle: { color: '#409eff' },
        z: 3
      },
      {
        name: '预测值',
        type: 'line',
        data: predValFull,
        smooth: true,
        lineStyle: { color: '#f56c6c', width: 2.5, type: 'dashed' },
        itemStyle: { color: '#f56c6c' },
        z: 3
      },
      {
        name: '置信上界',
        type: 'line',
        data: upperFull,
        smooth: true,
        lineStyle: { opacity: 0 },
        itemStyle: { opacity: 0 },
        areaStyle: { color: '#e6a23c', opacity: 0.15 },
        stack: 'confidence',
        z: 1
      },
      {
        name: '置信下界',
        type: 'line',
        data: lowerFull,
        smooth: true,
        lineStyle: { opacity: 0 },
        itemStyle: { opacity: 0 },
        areaStyle: { color: '#fff', opacity: 1 },
        stack: 'confidence',
        z: 1
      },
      // 预警线
      {
        name: '预警下限',
        type: 'line',
        data: allTimes.map(() => cfg.warnMin),
        lineStyle: { color: '#e6a23c', type: 'dotted', width: 1.5 },
        itemStyle: { opacity: 0 },
        z: 2
      },
      {
        name: '预警上限',
        type: 'line',
        data: allTimes.map(() => cfg.warnMax),
        lineStyle: { color: '#e6a23c', type: 'dotted', width: 1.5 },
        itemStyle: { opacity: 0 },
        z: 2
      }
    ]
  })
}

onMounted(() => {
  predChart = echarts.init(predictionChartRef.value)
  refreshChart()
  window.addEventListener('resize', () => predChart?.resize())
})

onUnmounted(() => {
  predChart?.dispose()
})
</script>

<style scoped>
.water-prediction { display: flex; flex-direction: column; gap: 16px; }
.param-card {}
.kpi-card {}
.kpi-inner { text-align: center; padding: 4px 0; }
.kpi-label { font-size: 12px; color: #888; }
.kpi-value { font-size: 26px; font-weight: 700; margin: 6px 0; }
.kpi-desc { font-size: 11px; color: #aaa; }
.chart-card {}
.chart-container { height: 400px; width: 100%; }
.chart-header { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px; }
.chart-title { display: flex; align-items: center; gap: 6px; font-weight: 600; font-size: 14px; }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 12px; color: #666; }
.legend-dot { display: inline-block; width: 20px; height: 3px; border-radius: 2px; }
.pred-value { color: #f56c6c; font-weight: 600; }
</style>

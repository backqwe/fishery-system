<template>
  <div class="water-trend">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">水质趋势分析</span>
          <el-radio-group v-model="selectedPond" size="small">
            <el-radio-button label="1号鱼塘" value="1号鱼塘" />
            <el-radio-button label="2号鱼塘" value="2号鱼塘" />
            <el-radio-button label="4号鱼塘" value="4号鱼塘" />
          </el-radio-group>
        </div>
      </template>

      <el-row :gutter="16">
        <el-col :xs="24" :md="12" style="margin-bottom:16px">
          <el-card shadow="hover">
            <template #header><span>水温趋势 (°C)</span></template>
            <div ref="tempChartRef" style="height:220px"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="12" style="margin-bottom:16px">
          <el-card shadow="hover">
            <template #header><span>pH值趋势</span></template>
            <div ref="phChartRef" style="height:220px"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="12" style="margin-bottom:16px">
          <el-card shadow="hover">
            <template #header><span>溶氧量趋势 (mg/L)</span></template>
            <div ref="doChartRef" style="height:220px"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="12" style="margin-bottom:16px">
          <el-card shadow="hover">
            <template #header><span>氨氮趋势 (mg/L)</span></template>
            <div ref="anChartRef" style="height:220px"></div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { waterTrendData } from '@/mock/water.js'

const selectedPond = ref('1号鱼塘')

const tempChartRef = ref(null)
const phChartRef = ref(null)
const doChartRef = ref(null)
const anChartRef = ref(null)

let charts = []

const lineOption = (seriesName, data, color) => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: waterTrendData.dates },
  yAxis: { type: 'value', scale: true },
  series: [{
    name: seriesName, type: 'line', data, smooth: true,
    itemStyle: { color },
    areaStyle: { color: color + '22' }
  }]
})

const initCharts = () => {
  charts.forEach(c => c?.dispose())
  charts = []

  const tc = echarts.init(tempChartRef.value)
  tc.setOption(lineOption('水温', waterTrendData.temperature, '#409eff'))
  charts.push(tc)

  const pc = echarts.init(phChartRef.value)
  pc.setOption(lineOption('pH', waterTrendData.ph, '#67c23a'))
  charts.push(pc)

  const dc = echarts.init(doChartRef.value)
  dc.setOption(lineOption('溶氧量', waterTrendData.dissolvedOxygen, '#e6a23c'))
  charts.push(dc)

  const ac = echarts.init(anChartRef.value)
  ac.setOption(lineOption('氨氮', waterTrendData.ammoniaNitrogen, '#f56c6c'))
  charts.push(ac)
}

const handleResize = () => charts.forEach(c => c?.resize())

watch(selectedPond, () => {
  setTimeout(initCharts, 50)
})

onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  charts.forEach(c => c?.dispose())
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
.title { font-size: 16px; font-weight: 600; }
</style>

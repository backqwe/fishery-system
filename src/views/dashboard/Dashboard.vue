<template>
  <div class="dashboard">
    <div class="page-title">首页 / 仪表盘</div>

    <!-- 统计卡片 -->
    <el-row :gutter="16" class="stat-cards">
      <el-col :xs="12" :sm="6" v-for="card in statCards" :key="card.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-card-inner">
            <div class="stat-icon" :style="{ background: card.bgColor }">
              <el-icon size="28" color="#fff"><component :is="card.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-title">{{ card.title }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="16" class="charts-row">
      <el-col :xs="24" :md="16">
        <el-card shadow="hover">
          <template #header>
            <span class="card-title">月度产量统计（kg）</span>
          </template>
          <div ref="yieldChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card shadow="hover">
          <template #header>
            <span class="card-title">养殖品种分布</span>
          </template>
          <div ref="speciesChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="charts-row">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <template #header>
            <span class="card-title">近7日投喂量趋势（kg）</span>
          </template>
          <div ref="feedChartRef" class="chart-container"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header-with-action">
              <span class="card-title">最近预警通知</span>
              <el-button type="primary" link size="small" @click="$router.push('/water/realtime')">查看全部</el-button>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="alert in recentAlerts"
              :key="alert.id"
              :type="alert.level === 'error' ? 'danger' : alert.level === 'warning' ? 'warning' : 'primary'"
              :timestamp="alert.time"
              placement="top"
            >
              <div class="alert-item">
                <el-tag :type="alert.level === 'error' ? 'danger' : alert.level === 'warning' ? 'warning' : 'info'" size="small">
                  {{ alert.type }}
                </el-tag>
                <span class="alert-pond">{{ alert.pond }}</span>
                <p class="alert-content">{{ alert.content }}</p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { dashboardStats, recentAlerts, yieldData, speciesDistribution, feedTrend } from '@/mock/dashboard.js'

const yieldChartRef = ref(null)
const speciesChartRef = ref(null)
const feedChartRef = ref(null)

let yieldChart, speciesChart, feedChart

const statCards = computed(() => [
  { title: '鱼塘总数', value: dashboardStats.pondCount, icon: 'Grid', bgColor: '#409eff' },
  { title: '养殖品种数', value: dashboardStats.speciesCount, icon: 'Crop', bgColor: '#67c23a' },
  { title: '今日投喂量(kg)', value: dashboardStats.todayFeed, icon: 'Food', bgColor: '#e6a23c' },
  { title: '当前预警数', value: dashboardStats.warningCount, icon: 'Warning', bgColor: '#f56c6c' }
])

const initYieldChart = () => {
  yieldChart = echarts.init(yieldChartRef.value)
  yieldChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: yieldData.months },
    yAxis: { type: 'value' },
    series: [{
      name: '产量',
      type: 'bar',
      data: yieldData.yield,
      itemStyle: { color: '#409eff' },
      label: { show: true, position: 'top' }
    }]
  })
}

const initSpeciesChart = () => {
  speciesChart = echarts.init(speciesChartRef.value)
  speciesChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}%' },
    legend: { orient: 'vertical', right: '5%', top: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: speciesDistribution,
      label: { show: false }
    }]
  })
}

const initFeedChart = () => {
  feedChart = echarts.init(feedChartRef.value)
  feedChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: feedTrend.dates },
    yAxis: { type: 'value' },
    series: [{
      name: '投喂量',
      type: 'line',
      data: feedTrend.amounts,
      smooth: true,
      itemStyle: { color: '#67c23a' },
      areaStyle: { color: 'rgba(103,194,58,0.1)' }
    }]
  })
}

const handleResize = () => {
  yieldChart?.resize()
  speciesChart?.resize()
  feedChart?.resize()
}

onMounted(() => {
  initYieldChart()
  initSpeciesChart()
  initFeedChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  yieldChart?.dispose()
  speciesChart?.dispose()
  feedChart?.dispose()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.page-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 16px;
}

.stat-cards {
  margin-bottom: 16px;
}

.stat-card {
  margin-bottom: 16px;
}

.stat-card-inner {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-title {
  font-size: 13px;
  color: #999;
}

.charts-row {
  margin-bottom: 16px;
}

.chart-container {
  height: 280px;
}

.card-title {
  font-weight: 600;
  font-size: 15px;
}

.card-header-with-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.alert-item {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.alert-pond {
  font-weight: 500;
  color: #333;
}

.alert-content {
  width: 100%;
  margin: 4px 0 0;
  color: #666;
  font-size: 13px;
}
</style>

<template>
  <div class="dashboard">
    <div class="page-title">仪表盘</div>

    <!-- Stats Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in stats" :key="stat.title">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-info">
              <div class="stat-title">{{ stat.title }}</div>
              <div class="stat-value">{{ stat.value }}<span class="stat-unit">{{ stat.unit }}</span></div>
              <div class="stat-trend" :class="stat.trend.startsWith('+') ? 'up' : 'down'">
                较昨日 {{ stat.trend }}
              </div>
            </div>
            <div class="stat-icon" :style="{ background: stat.color }">
              <el-icon size="28"><component :is="stat.icon" /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row -->
    <el-row :gutter="20" class="chart-row">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <span>年度产量趋势</span>
          </template>
          <v-chart :option="productionChartOption" style="height: 300px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <span>鱼塘状态分布</span>
          </template>
          <v-chart :option="pondStatusChartOption" style="height: 300px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- Alerts -->
    <el-card shadow="hover" class="alert-card">
      <template #header>
        <div class="card-header">
          <span>最近预警</span>
          <el-button type="primary" link>查看全部</el-button>
        </div>
      </template>
      <el-table :data="alerts" stripe>
        <el-table-column prop="pond" label="鱼塘" width="100" />
        <el-table-column prop="type" label="预警类型" width="120" />
        <el-table-column prop="message" label="预警信息" />
        <el-table-column prop="time" label="时间" width="120" />
        <el-table-column label="级别" width="80">
          <template #default="{ row }">
            <el-tag :type="row.level === 'danger' ? 'danger' : 'warning'" size="small">
              {{ row.level === 'danger' ? '严重' : '警告' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default>
            <el-button type="primary" link size="small">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { statsData, productionData, pondStatusData, recentAlerts } from '@/mock/dashboard'

const stats = statsData
const alerts = recentAlerts

const productionChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: productionData.series.map(s => s.name) },
  xAxis: { type: 'category', data: productionData.months },
  yAxis: { type: 'value', name: '产量(kg)' },
  series: productionData.series.map(s => ({
    name: s.name,
    type: 'line',
    smooth: true,
    data: s.data
  }))
}))

const pondStatusChartOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  legend: { bottom: 0 },
  series: [{
    type: 'pie',
    radius: ['40%', '70%'],
    data: pondStatusData,
    emphasis: {
      itemStyle: {
        shadowBlur: 10,
        shadowOffsetX: 0,
        shadowColor: 'rgba(0, 0, 0, 0.5)'
      }
    }
  }]
}))
</script>

<style scoped>
.dashboard { }
.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}
.stats-row { margin-bottom: 20px; }
.stat-card :deep(.el-card__body) { padding: 20px; }
.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.stat-title { color: #666; font-size: 14px; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: bold; color: #333; }
.stat-unit { font-size: 14px; color: #666; margin-left: 4px; }
.stat-trend { font-size: 12px; margin-top: 4px; }
.stat-trend.up { color: #f56c6c; }
.stat-trend.down { color: #67c23a; }
.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}
.chart-row { margin-bottom: 20px; }
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

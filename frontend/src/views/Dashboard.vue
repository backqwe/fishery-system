<template>
  <div class="page-container">
    <el-row :gutter="16" class="stat-row">
      <el-col :span="6" v-for="item in statCards" :key="item.label">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: item.color }">
              <el-icon size="28" color="#fff"><component :is="item.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ item.value }}</div>
              <div class="stat-label">{{ item.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top:16px">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header><span>产量趋势（近12个月）</span></template>
          <v-chart class="chart" :option="trendOption" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span>养殖品种分布</span></template>
          <v-chart class="chart" :option="pieOption" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="hover" style="margin-top:16px">
      <template #header>
        <span>最近预警通知</span>
        <el-tag type="danger" style="margin-left:8px">{{ recentAlerts.length }}</el-tag>
      </template>
      <el-table :data="recentAlerts" stripe>
        <el-table-column prop="pond" label="鱼塘" width="120" />
        <el-table-column prop="type" label="预警类型" width="150" />
        <el-table-column prop="value" label="当前值" width="120" />
        <el-table-column prop="time" label="时间" />
        <el-table-column label="级别" width="100">
          <template #default="{ row }">
            <el-tag :type="row.level === 'danger' ? 'danger' : row.level === 'warning' ? 'warning' : 'info'" size="small">
              {{ row.level === 'danger' ? '严重' : row.level === 'warning' ? '预警' : '提示' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default>
            <el-button type="primary" text size="small">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { stats, productionTrend, speciesDistribution, recentAlerts } from '@/mock/dashboard.js'

const statCards = [
  { label: '鱼塘数量（个）', value: stats.pondCount, icon: 'Grid', color: '#1890ff' },
  { label: '养殖品种数', value: stats.speciesCount, icon: 'Crop', color: '#52c41a' },
  { label: '今日投喂量（kg）', value: stats.todayFeed.toLocaleString(), icon: 'TrendCharts', color: '#fa8c16' },
  { label: '预警数量', value: stats.alertCount, icon: 'Bell', color: '#f5222d' }
]

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: productionTrend.months },
  yAxis: { type: 'value', name: '产量(kg)' },
  series: [{ name: '产量', type: 'line', data: productionTrend.data, smooth: true, areaStyle: { opacity: 0.3 }, itemStyle: { color: '#1890ff' } }]
}))

const pieOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c}% ({d}%)' },
  legend: { orient: 'vertical', right: 10, top: 'center' },
  series: [{
    type: 'pie', radius: ['40%', '70%'], center: ['40%', '50%'],
    data: speciesDistribution,
    label: { show: false }
  }]
}))
</script>

<style scoped>
.stat-row { margin-bottom: 0; }
.stat-card .stat-content { display: flex; align-items: center; gap: 16px; }
.stat-icon { width: 60px; height: 60px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
.stat-value { font-size: 28px; font-weight: 700; color: #262626; line-height: 1; }
.stat-label { font-size: 13px; color: #8c8c8c; margin-top: 6px; }
.chart { height: 300px; }
</style>

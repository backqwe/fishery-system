<template>
  <div class="page-container">
    <el-row :gutter="16" style="margin-bottom:16px">
      <el-col :span="24">
        <el-alert title="实时水质监测 - 数据每5分钟自动刷新" type="info" :closable="false" show-icon />
      </el-col>
    </el-row>

    <el-card shadow="hover" style="margin-bottom:16px">
      <template #header>水质参数总览</template>
      <el-table :data="realtimeData" stripe border>
        <el-table-column prop="pondName" label="鱼塘" width="120" />
        <el-table-column label="水温(°C)" width="110">
          <template #default="{ row }">
            <span :class="row.temperature > 30 ? 'text-danger' : ''">{{ row.temperature }}</span>
          </template>
        </el-table-column>
        <el-table-column label="pH值" width="90">
          <template #default="{ row }">
            <span :class="(row.ph < 6.5 || row.ph > 9.0) ? 'text-danger' : ''">{{ row.ph }}</span>
          </template>
        </el-table-column>
        <el-table-column label="溶氧量(mg/L)" width="130">
          <template #default="{ row }">
            <span :class="row.oxygen < 5 ? 'text-danger' : ''">{{ row.oxygen }}</span>
          </template>
        </el-table-column>
        <el-table-column label="氨氮(mg/L)" width="120">
          <template #default="{ row }">
            <span :class="row.ammonia > 0.5 ? 'text-danger' : ''">{{ row.ammonia }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="turbidity" label="浑浊度(NTU)" width="130" />
        <el-table-column prop="updateTime" label="更新时间" width="180" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === '正常' ? 'success' : row.status === '预警' ? 'warning' : 'danger'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="hover">
      <template #header>1号鱼塘 - 今日水质趋势</template>
      <v-chart class="chart" :option="trendOption" autoresize />
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { realtimeData, trendData } from '@/mock/water.js'

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['水温', 'pH值', '溶氧量'] },
  xAxis: { type: 'category', data: trendData.times },
  yAxis: { type: 'value' },
  series: [
    { name: '水温', type: 'line', data: trendData.temperature, smooth: true, itemStyle: { color: '#ff7875' } },
    { name: 'pH值', type: 'line', data: trendData.ph, smooth: true, itemStyle: { color: '#69c0ff' } },
    { name: '溶氧量', type: 'line', data: trendData.oxygen, smooth: true, itemStyle: { color: '#95de64' } }
  ]
}))
</script>

<style scoped>
.chart { height: 280px; }
.text-danger { color: #f5222d; font-weight: bold; }
</style>

<template>
  <div>
    <div class="page-title">水质趋势分析</div>
    <el-card shadow="hover" style="margin-bottom: 20px">
      <el-form :inline="true">
        <el-form-item label="鱼塘">
          <el-select v-model="selectedPond" style="width: 140px">
            <el-option label="1号鱼塘" value="1" />
            <el-option label="2号鱼塘" value="2" />
            <el-option label="3号鱼塘" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-select v-model="timeRange" style="width: 120px">
            <el-option label="今日" value="day" />
            <el-option label="近7天" value="week" />
            <el-option label="近30天" value="month" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="12" style="margin-bottom: 20px">
        <el-card shadow="hover" header="水温趋势">
          <v-chart :option="tempChartOption" style="height: 250px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12" style="margin-bottom: 20px">
        <el-card shadow="hover" header="pH值趋势">
          <v-chart :option="phChartOption" style="height: 250px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" header="溶氧量趋势">
          <v-chart :option="doChartOption" style="height: 250px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" header="氨氮趋势">
          <v-chart :option="anChartOption" style="height: 250px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import VChart from 'vue-echarts'
import { waterQualityTrend } from '@/mock/waterquality'

const selectedPond = ref('1')
const timeRange = ref('day')
const trend = waterQualityTrend

const makeLineChart = (name: string, data: number[], color: string) => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: trend.times },
  yAxis: { type: 'value' },
  series: [{ name, type: 'line', smooth: true, data, lineStyle: { color }, itemStyle: { color } }]
})

const tempChartOption = computed(() => makeLineChart('水温(°C)', trend.temperature, '#ff7c7c'))
const phChartOption = computed(() => makeLineChart('pH值', trend.pH, '#5b9bd5'))
const doChartOption = computed(() => makeLineChart('溶氧量(mg/L)', trend.dissolvedOxygen, '#4caf50'))
const anChartOption = computed(() => makeLineChart('氨氮(mg/L)', trend.ammoniaNitrogen, '#ff9800'))
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
</style>

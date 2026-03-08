<template>
  <div>
    <div class="page-title">水质实时监测</div>
    <div class="update-time">最后更新: 2024-03-01 14:30:00 <el-button type="primary" link>刷新</el-button></div>

    <el-row :gutter="20">
      <el-col :span="12" v-for="pond in waterQuality" :key="pond.pondId" style="margin-bottom: 20px">
        <el-card shadow="hover" :class="pond.status === '预警' ? 'warning-card' : ''">
          <template #header>
            <div class="card-header">
              <span>{{ pond.pondName }}</span>
              <el-tag :type="pond.status === '正常' ? 'success' : pond.status === '预警' ? 'danger' : 'info'">
                {{ pond.status }}
              </el-tag>
            </div>
          </template>
          <el-row :gutter="16">
            <el-col :span="12" v-for="param in getParams(pond)" :key="param.label">
              <div class="param-item" :class="param.alert ? 'param-alert' : ''">
                <div class="param-label">{{ param.label }}</div>
                <div class="param-value">{{ param.value }}<span class="param-unit">{{ param.unit }}</span></div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { currentWaterQuality } from '@/mock/waterquality'

const waterQuality = currentWaterQuality

const getParams = (pond: any) => [
  { label: '水温', value: pond.temperature, unit: '°C', alert: pond.temperature > 28 },
  { label: 'pH值', value: pond.pH, unit: '', alert: pond.pH > 8.5 || pond.pH < 6.5 },
  { label: '溶氧量', value: pond.dissolvedOxygen, unit: 'mg/L', alert: pond.dissolvedOxygen < 5 },
  { label: '氨氮', value: pond.ammoniaNitrogen, unit: 'mg/L', alert: pond.ammoniaNitrogen > 1.0 },
  { label: '浊度', value: pond.turbidity, unit: 'NTU', alert: pond.turbidity > 30 },
]
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 8px; color: #333; }
.update-time { color: #999; font-size: 13px; margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.warning-card { border-color: #f56c6c; }
.param-item {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 12px;
  text-align: center;
}
.param-alert { background: #fff0f0; border: 1px solid #ffccc7; }
.param-label { color: #666; font-size: 12px; margin-bottom: 4px; }
.param-value { font-size: 22px; font-weight: bold; color: #333; }
.param-alert .param-value { color: #f56c6c; }
.param-unit { font-size: 12px; color: #666; }
</style>

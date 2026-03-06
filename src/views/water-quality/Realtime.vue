<template>
  <div class="water-realtime">
    <div class="page-header">
      <span class="title">水质实时数据</span>
      <el-button @click="refreshData" :loading="refreshing">
        <el-icon><Refresh /></el-icon>刷新
      </el-button>
    </div>

    <el-row :gutter="16">
      <el-col :xs="24" :sm="12" :lg="8" v-for="item in waterData" :key="item.pondId" style="margin-bottom:16px">
        <el-card shadow="hover" :class="['water-card', item.status === '预警' ? 'warning-card' : '']">
          <div class="water-card-header">
            <span class="pond-name">{{ item.pondName }}</span>
            <el-tag :type="item.status === '正常' ? 'success' : 'danger'" size="small">{{ item.status }}</el-tag>
          </div>
          <div class="params-grid">
            <div class="param-item">
              <div class="param-label">水温</div>
              <div class="param-value" :class="getClass(item.temperature, 18, 28)">{{ item.temperature }}°C</div>
            </div>
            <div class="param-item">
              <div class="param-label">pH值</div>
              <div class="param-value" :class="getClass(item.ph, 6.5, 8.5)">{{ item.ph }}</div>
            </div>
            <div class="param-item">
              <div class="param-label">溶氧量</div>
              <div class="param-value" :class="getClass(item.dissolvedOxygen, 5, 12)">{{ item.dissolvedOxygen }} mg/L</div>
            </div>
            <div class="param-item">
              <div class="param-label">氨氮</div>
              <div class="param-value" :class="item.ammoniaNitrogen > 0.2 ? 'val-warning' : 'val-normal'">{{ item.ammoniaNitrogen }} mg/L</div>
            </div>
            <div class="param-item">
              <div class="param-label">浑浊度</div>
              <div class="param-value" :class="item.turbidity > 40 ? 'val-warning' : 'val-normal'">{{ item.turbidity }} NTU</div>
            </div>
          </div>
          <div class="update-time">更新时间：{{ item.updateTime }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { waterQualityRealtime } from '@/mock/water.js'

const waterData = ref([...waterQualityRealtime])
const refreshing = ref(false)

const refreshData = () => {
  refreshing.value = true
  setTimeout(() => {
    // Simulate data update with small random fluctuations
    waterData.value = waterData.value.map(item => ({
      ...item,
      temperature: +(item.temperature + (Math.random() - 0.5) * 0.4).toFixed(1),
      ph: +(item.ph + (Math.random() - 0.5) * 0.1).toFixed(1),
      dissolvedOxygen: +(item.dissolvedOxygen + (Math.random() - 0.5) * 0.3).toFixed(1),
      updateTime: new Date().toLocaleString('zh-CN')
    }))
    refreshing.value = false
    ElMessage.success('数据已刷新')
  }, 600)
}

const getClass = (value, min, max) => {
  return (value < min || value > max) ? 'val-warning' : 'val-normal'
}
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.title {
  font-size: 18px;
  font-weight: 600;
}
.water-card {
  transition: box-shadow 0.2s;
}
.warning-card {
  border: 1px solid #f56c6c;
}
.water-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.pond-name {
  font-size: 16px;
  font-weight: 600;
}
.params-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}
.param-item {
  text-align: center;
}
.param-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}
.param-value {
  font-size: 16px;
  font-weight: 600;
}
.val-normal {
  color: #67c23a;
}
.val-warning {
  color: #f56c6c;
}
.update-time {
  font-size: 12px;
  color: #aaa;
  text-align: right;
}
</style>

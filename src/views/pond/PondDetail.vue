<template>
  <div class="pond-detail">
    <div class="page-header">
      <el-button @click="$router.push('/pond/list')" link>
        <el-icon><ArrowLeft /></el-icon>返回列表
      </el-button>
    </div>

    <el-row :gutter="16">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="info-card">
          <template #header><span class="card-title">基本信息</span></template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="鱼塘名称">{{ pond.name }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusTagType(pond.status)" size="small">{{ pond.status }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="面积">{{ pond.area }} 亩</el-descriptions-item>
            <el-descriptions-item label="水深">{{ pond.depth }} m</el-descriptions-item>
            <el-descriptions-item label="类型">{{ pond.type }}</el-descriptions-item>
            <el-descriptions-item label="位置">{{ pond.location }}</el-descriptions-item>
            <el-descriptions-item label="存塘数量">{{ pond.fishCount }} 尾</el-descriptions-item>
            <el-descriptions-item label="负责人">{{ pond.manager }}</el-descriptions-item>
            <el-descriptions-item label="建立时间" :span="2">{{ pond.createTime }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card shadow="hover" class="info-card">
          <template #header><span class="card-title">当前水质参数</span></template>
          <el-descriptions :column="1" border v-if="waterData">
            <el-descriptions-item label="水温">
              <span :class="getParamClass(waterData.temperature, 18, 28)">{{ waterData.temperature }} °C</span>
            </el-descriptions-item>
            <el-descriptions-item label="pH值">
              <span :class="getParamClass(waterData.ph, 6.5, 8.5)">{{ waterData.ph }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="溶氧量">
              <span :class="getParamClass(waterData.dissolvedOxygen, 5, 12)">{{ waterData.dissolvedOxygen }} mg/L</span>
            </el-descriptions-item>
            <el-descriptions-item label="氨氮">
              <span :class="getParamClass(waterData.ammoniaNitrogen, 0, 0.2, true)">{{ waterData.ammoniaNitrogen }} mg/L</span>
            </el-descriptions-item>
            <el-descriptions-item label="浑浊度">
              <span :class="getParamClass(waterData.turbidity, 0, 40, true)">{{ waterData.turbidity }} NTU</span>
            </el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ waterData.updateTime }}</el-descriptions-item>
          </el-descriptions>
          <el-empty v-else description="暂无水质数据" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ponds } from '@/mock/pond.js'
import { waterQualityRealtime } from '@/mock/water.js'

const route = useRoute()
const pondId = parseInt(route.params.id)

const pond = computed(() => ponds.find(p => p.id === pondId) || {})
const waterData = computed(() => waterQualityRealtime.find(w => w.pondId === pondId))

const statusTagType = (status) => {
  const map = { 正常: 'success', 预警: 'warning', 维护: 'info' }
  return map[status] || 'info'
}

const getParamClass = (value, min, max, reverseWarning = false) => {
  if (reverseWarning) {
    return value > max ? 'param-warning' : 'param-normal'
  }
  return (value < min || value > max) ? 'param-warning' : 'param-normal'
}
</script>

<style scoped>
.page-header {
  margin-bottom: 16px;
}
.info-card {
  margin-bottom: 16px;
}
.card-title {
  font-size: 15px;
  font-weight: 600;
}
.param-normal {
  color: #67c23a;
  font-weight: 500;
}
.param-warning {
  color: #f56c6c;
  font-weight: 500;
}
</style>

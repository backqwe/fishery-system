<template>
  <div class="page-container">
    <el-page-header @back="$router.back()" content="鱼塘详情" style="margin-bottom:16px" />
    <el-row :gutter="16">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>基本信息</template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="鱼塘名称">{{ detail.name }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="detail.status === '正常' ? 'success' : 'warning'">{{ detail.status }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="面积">{{ detail.area }} 亩</el-descriptions-item>
            <el-descriptions-item label="深度">{{ detail.depth }} m</el-descriptions-item>
            <el-descriptions-item label="位置">{{ detail.location }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ detail.createTime }}</el-descriptions-item>
            <el-descriptions-item label="养殖品种">{{ detail.species }}</el-descriptions-item>
            <el-descriptions-item label="放养数量">{{ detail.quantity }} 条</el-descriptions-item>
            <el-descriptions-item label="预估总重">{{ detail.weight }} kg</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>当前水质参数</template>
          <el-row :gutter="12">
            <el-col :span="12" v-for="param in waterParams" :key="param.label" style="margin-bottom:12px">
              <div class="param-card" :style="{ borderLeft: `4px solid ${param.color}` }">
                <div class="param-value">{{ param.value }}<span class="param-unit">{{ param.unit }}</span></div>
                <div class="param-label">{{ param.label }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { pondDetail } from '@/mock/pond.js'

const detail = pondDetail

const waterParams = computed(() => [
  { label: '水温', value: detail.waterParams.temperature, unit: '°C', color: '#ff7875' },
  { label: 'pH值', value: detail.waterParams.ph, unit: '', color: '#69c0ff' },
  { label: '溶氧量', value: detail.waterParams.oxygen, unit: 'mg/L', color: '#95de64' },
  { label: '氨氮', value: detail.waterParams.ammonia, unit: 'mg/L', color: '#ffd666' },
  { label: '浑浊度', value: detail.waterParams.turbidity, unit: 'NTU', color: '#b37feb' },
  { label: '水位', value: detail.waterParams.waterLevel, unit: 'm', color: '#5cdbd3' }
])
</script>

<style scoped>
.param-card { padding: 12px 16px; background: #fafafa; border-radius: 4px; }
.param-value { font-size: 22px; font-weight: 700; color: #262626; }
.param-unit { font-size: 12px; color: #8c8c8c; margin-left: 4px; }
.param-label { font-size: 12px; color: #8c8c8c; margin-top: 4px; }
</style>

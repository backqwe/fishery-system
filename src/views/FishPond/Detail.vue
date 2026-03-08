<template>
  <div>
    <div class="page-header">
      <el-button @click="$router.back()"><el-icon><ArrowLeft /></el-icon>返回</el-button>
      <span class="page-title">鱼塘详情</span>
    </div>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover" header="基本信息">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="鱼塘名称">{{ detail.name }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusType(detail.status)">{{ detail.status }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="面积">{{ detail.area }} 亩</el-descriptions-item>
            <el-descriptions-item label="水深">{{ detail.depth }} m</el-descriptions-item>
            <el-descriptions-item label="类型">{{ detail.type }}</el-descriptions-item>
            <el-descriptions-item label="养殖品种">{{ detail.species }}</el-descriptions-item>
            <el-descriptions-item label="存栏数量">{{ detail.stockQuantity }} 尾</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ detail.createTime }}</el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ detail.notes }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" header="水质参数">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="水温">{{ detail.waterTemp }} °C</el-descriptions-item>
            <el-descriptions-item label="pH值">{{ detail.pH }}</el-descriptions-item>
            <el-descriptions-item label="溶氧量">{{ detail.dissolvedOxygen }} mg/L</el-descriptions-item>
            <el-descriptions-item label="氨氮">{{ detail.ammoniaNitrogen }} mg/L</el-descriptions-item>
            <el-descriptions-item label="浊度">{{ detail.turbidity }} NTU</el-descriptions-item>
            <el-descriptions-item label="日投喂量">{{ detail.feedingPerDay }} kg</el-descriptions-item>
            <el-descriptions-item label="最近投喂" :span="2">{{ detail.lastFeedingTime }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { getPondDetail } from '@/mock/fishpond'

const route = useRoute()
const id = Number(route.params.id)
const detail = computed(() => getPondDetail(id))

const statusType = (status: string | undefined) => {
  const map: Record<string, string> = { '正常': 'success', '预警': 'warning', '维护': 'info', '空置': '' }
  return map[status || ''] || ''
}
</script>

<style scoped>
.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.page-title { font-size: 20px; font-weight: bold; color: #333; }
</style>

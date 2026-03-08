<template>
  <div>
    <div class="page-title">预警阈值设置</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>预警参数配置</span>
          <el-button type="primary" @click="handleSave">保存设置</el-button>
        </div>
      </template>
      <el-table :data="thresholds" stripe>
        <el-table-column prop="parameter" label="监测参数" width="120" />
        <el-table-column label="最小值" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.minValue" :step="0.1" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="最大值" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.maxValue" :step="0.1" size="small" />
          </template>
        </el-table-column>
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column label="是否启用" width="100">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default>
            <el-button type="primary" link size="small">重置</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { alertThresholds } from '@/mock/waterquality'

const thresholds = ref(alertThresholds.map(t => ({ ...t })))

const handleSave = () => {
  ElMessage.success('预警设置已保存')
}
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

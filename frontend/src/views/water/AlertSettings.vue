<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>预警阈值设置</span>
          <el-button type="primary" @click="handleSaveAll">保存设置</el-button>
        </div>
      </template>
      <el-table :data="thresholds" border>
        <el-table-column prop="param" label="参数名称" width="120" />
        <el-table-column prop="unit" label="单位" width="80" />
        <el-table-column label="最小值" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.minValue" :step="0.1" size="small" style="width:120px" />
          </template>
        </el-table-column>
        <el-table-column label="最大值" width="160">
          <template #default="{ row }">
            <el-input-number v-model="row.maxValue" :step="0.1" size="small" style="width:120px" />
          </template>
        </el-table-column>
        <el-table-column label="启用状态" width="120">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { alertThresholds } from '@/mock/water.js'

const thresholds = ref(alertThresholds.map(t => ({ ...t })))

const handleSaveAll = () => ElMessage.success('预警设置已保存')
</script>

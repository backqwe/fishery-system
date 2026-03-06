<template>
  <div class="water-threshold">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">预警阈值设置</span>
          <el-button type="primary" @click="handleSave" :loading="saving">保存设置</el-button>
        </div>
      </template>

      <el-alert type="info" show-icon :closable="false" style="margin-bottom:16px">
        <template #title>当水质参数超出预警范围时，系统将自动发送预警通知。请合理设置各项参数的阈值。</template>
      </el-alert>

      <el-table :data="thresholds" border stripe>
        <el-table-column prop="label" label="参数名称" width="120" />
        <el-table-column prop="unit" label="单位" width="80" align="center">
          <template #default="{ row }">{{ row.unit || '—' }}</template>
        </el-table-column>
        <el-table-column label="正常范围" min-width="180">
          <template #default="{ row }">
            <div class="range-inputs">
              <el-input-number
                v-model="row.minValue" :precision="1" size="small" style="width:100px"
                controls-position="right"
              />
              <span>~</span>
              <el-input-number
                v-model="row.maxValue" :precision="1" size="small" style="width:100px"
                controls-position="right"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="预警范围" min-width="180">
          <template #default="{ row }">
            <div class="range-inputs">
              <el-input-number
                v-model="row.warningMin" :precision="1" size="small" style="width:100px"
                controls-position="right"
              />
              <span>~</span>
              <el-input-number
                v-model="row.warningMax" :precision="1" size="small" style="width:100px"
                controls-position="right"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template #default>
            <el-tag type="success" size="small">已启用</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { waterThresholds } from '@/mock/water.js'

const thresholds = ref(waterThresholds.map(t => ({ ...t })))
const saving = ref(false)

const handleSave = () => {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    ElMessage.success('预警阈值设置已保存')
  }, 600)
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
.range-inputs { display: flex; align-items: center; gap: 8px; }
</style>

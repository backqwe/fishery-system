<template>
  <div class="growth-monitor">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">生长监测</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>添加监测记录
          </el-button>
        </div>
      </template>

      <el-row :gutter="16" style="margin-bottom:16px">
        <el-col :span="6">
          <el-select v-model="selectedBatch" placeholder="选择批次" style="width:100%" @change="updateChart">
            <el-option v-for="b in batchOptions" :key="b.value" :label="b.label" :value="b.value" />
          </el-select>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :xs="24" :md="12">
          <el-card shadow="hover" style="margin-bottom:16px">
            <template #header><span>平均体重增长趋势（kg）</span></template>
            <div ref="weightChartRef" style="height:240px"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="12">
          <el-card shadow="hover" style="margin-bottom:16px">
            <template #header><span>存活率趋势（%）</span></template>
            <div ref="survivalChartRef" style="height:240px"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-table :data="tableData" stripe border>
        <el-table-column prop="date" label="监测日期" width="120" align="center" />
        <el-table-column prop="batchNo" label="批次号" min-width="140" />
        <el-table-column prop="sampleCount" label="抽样数量(尾)" width="130" align="center" />
        <el-table-column prop="avgWeight" label="平均体重(kg)" width="130" align="center" />
        <el-table-column prop="avgLength" label="平均体长(cm)" width="130" align="center" />
        <el-table-column prop="survivalRate" label="存活率(%)" width="110" align="center">
          <template #default="{ row }">
            <span :style="{ color: row.survivalRate < 95 ? '#f56c6c' : '#67c23a' }">{{ row.survivalRate }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" min-width="140" show-overflow-tooltip />
      </el-table>
    </el-card>

    <el-dialog v-model="showAddDialog" title="添加生长监测记录" width="480px">
      <el-form :model="addForm" label-width="120px">
        <el-form-item label="批次号"><el-input v-model="addForm.batchNo" /></el-form-item>
        <el-form-item label="抽样数量"><el-input-number v-model="addForm.sampleCount" :min="1" style="width:100%" /></el-form-item>
        <el-form-item label="平均体重(kg)"><el-input-number v-model="addForm.avgWeight" :min="0.01" :precision="2" style="width:100%" /></el-form-item>
        <el-form-item label="平均体长(cm)"><el-input-number v-model="addForm.avgLength" :min="1" :precision="1" style="width:100%" /></el-form-item>
        <el-form-item label="存活率(%)"><el-input-number v-model="addForm.survivalRate" :min="0" :max="100" :precision="1" style="width:100%" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="addForm.note" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
import { growthData } from '@/mock/aquaculture.js'

const selectedBatch = ref('PC202401001')
const batchOptions = [
  { label: 'PC202401001 (1号鱼塘-草鱼)', value: 'PC202401001' },
  { label: 'PC202401002 (2号鱼塘-鲤鱼)', value: 'PC202401002' }
]

const records = ref([...growthData])
const showAddDialog = ref(false)
const addForm = ref({ batchNo: 'PC202401001', sampleCount: 20, avgWeight: 0.2, avgLength: 13.0, survivalRate: 98.0, note: '' })

const tableData = computed(() => records.value.filter(r => r.batchNo === selectedBatch.value))

const weightChartRef = ref(null)
const survivalChartRef = ref(null)
let weightChart, survivalChart

const initCharts = () => {
  const data = tableData.value.slice().reverse()
  const dates = data.map(d => d.date)
  const weights = data.map(d => d.avgWeight)
  const survivals = data.map(d => d.survivalRate)

  weightChart = echarts.init(weightChartRef.value)
  weightChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: dates },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: weights, smooth: true, itemStyle: { color: '#409eff' } }]
  })

  survivalChart = echarts.init(survivalChartRef.value)
  survivalChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: dates },
    yAxis: { type: 'value', min: 90, max: 100 },
    series: [{ type: 'line', data: survivals, smooth: true, itemStyle: { color: '#67c23a' } }]
  })
}

const updateChart = () => {
  weightChart?.dispose()
  survivalChart?.dispose()
  setTimeout(initCharts, 50)
}

const handleAdd = () => {
  records.value.unshift({ id: Date.now(), date: new Date().toISOString().slice(0, 10), ...addForm.value })
  showAddDialog.value = false
  ElMessage.success('监测记录已添加')
  updateChart()
}

onMounted(initCharts)
onUnmounted(() => { weightChart?.dispose(); survivalChart?.dispose() })
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
</style>

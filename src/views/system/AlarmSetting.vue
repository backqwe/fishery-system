<template>
  <div class="alarm-setting">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">报警值设置</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增报警设置
          </el-button>
        </div>
      </template>

      <!-- 说明提示 -->
      <el-alert
        title="报警值设置说明：当监测数据超出设定阈值范围时，系统将自动触发报警通知。请根据养殖品种特性合理设置阈值。"
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom:16px"
      />

      <!-- 搜索 -->
      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="监测参数">
            <el-select v-model="searchForm.parameter" placeholder="全部参数" clearable style="width:160px">
              <el-option v-for="p in parameterOptions" :key="p.value" :label="p.label" :value="p.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="应用场景">
            <el-input v-model="searchForm.scene" placeholder="养殖场/品种" clearable style="width:150px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.enabled" placeholder="全部" clearable style="width:100px">
              <el-option label="启用" value="启用" />
              <el-option label="禁用" value="禁用" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 表格 -->
      <el-table :data="filteredData" stripe border style="width:100%">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="paramLabel" label="监测参数" width="120" />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
        <el-table-column prop="scene" label="应用场景" min-width="130" />
        <el-table-column label="正常范围" width="130" align="center">
          <template #default="{ row }">
            <span class="range-text">{{ row.normalMin }} ~ {{ row.normalMax }}</span>
          </template>
        </el-table-column>
        <el-table-column label="预警范围" width="130" align="center">
          <template #default="{ row }">
            <span class="range-text warn">{{ row.warnMin }} ~ {{ row.warnMax }}</span>
          </template>
        </el-table-column>
        <el-table-column label="报警范围" width="130" align="center">
          <template #default="{ row }">
            <span class="range-text error">{{ row.alarmMin }} ~ {{ row.alarmMax }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="报警级别" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.level === '严重' ? 'danger' : row.level === '重要' ? 'warning' : 'info'" size="small">
              {{ row.level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="notifyMethod" label="通知方式" min-width="120" />
        <el-table-column prop="enabled" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-switch
              :model-value="row.enabled === '启用'"
              @change="(val) => toggleEnabled(row, val)"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deleteRow(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrap">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="filteredData.length"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="580px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="监测参数" prop="parameter">
          <el-select v-model="form.parameter" placeholder="请选择" style="width:100%" @change="fillUnit">
            <el-option v-for="p in parameterOptions" :key="p.value" :label="p.label" :value="p.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" placeholder="如 °C, mg/L" />
        </el-form-item>
        <el-form-item label="应用场景" prop="scene">
          <el-input v-model="form.scene" placeholder="如 草鱼养殖、全部场景" />
        </el-form-item>
        <el-divider>正常范围</el-divider>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="正常最小值" prop="normalMin">
              <el-input-number v-model="form.normalMin" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="正常最大值" prop="normalMax">
              <el-input-number v-model="form.normalMax" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider>预警范围（触发预警通知）</el-divider>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="预警最小值" prop="warnMin">
              <el-input-number v-model="form.warnMin" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预警最大值" prop="warnMax">
              <el-input-number v-model="form.warnMax" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider>报警范围（触发紧急报警）</el-divider>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="报警最小值" prop="alarmMin">
              <el-input-number v-model="form.alarmMin" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报警最大值" prop="alarmMax">
              <el-input-number v-model="form.alarmMax" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="报警级别" prop="level">
          <el-radio-group v-model="form.level">
            <el-radio label="一般">一般</el-radio>
            <el-radio label="重要">重要</el-radio>
            <el-radio label="严重">严重</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="通知方式" prop="notifyMethod">
          <el-checkbox-group v-model="form.notifyMethods">
            <el-checkbox label="系统消息">系统消息</el-checkbox>
            <el-checkbox label="短信">短信</el-checkbox>
            <el-checkbox label="邮件">邮件</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="状态" prop="enabled">
          <el-radio-group v-model="form.enabled">
            <el-radio label="启用">启用</el-radio>
            <el-radio label="禁用">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// ===================== Mock 报警值设置数据 =====================
const parameterOptions = [
  { label: '水温', value: 'temperature', unit: '°C' },
  { label: 'pH值', value: 'ph', unit: '' },
  { label: '溶解氧', value: 'dissolvedOxygen', unit: 'mg/L' },
  { label: '氨氮', value: 'ammoniaNitrogen', unit: 'mg/L' },
  { label: '浑浊度', value: 'turbidity', unit: 'NTU' },
  { label: '亚硝酸盐', value: 'nitrite', unit: 'mg/L' },
  { label: '盐度', value: 'salinity', unit: '‰' },
]

const tableData = ref([
  { id: 1, parameter: 'temperature', paramLabel: '水温', unit: '°C', scene: '全部场景', normalMin: 18, normalMax: 28, warnMin: 16, warnMax: 30, alarmMin: 12, alarmMax: 35, level: '重要', notifyMethod: '系统消息,短信', enabled: '启用' },
  { id: 2, parameter: 'ph', paramLabel: 'pH值', unit: '', scene: '全部场景', normalMin: 6.8, normalMax: 8.5, warnMin: 6.5, warnMax: 9.0, alarmMin: 6.0, alarmMax: 9.5, level: '严重', notifyMethod: '系统消息,短信,邮件', enabled: '启用' },
  { id: 3, parameter: 'dissolvedOxygen', paramLabel: '溶解氧', unit: 'mg/L', scene: '全部场景', normalMin: 6.0, normalMax: 12.0, warnMin: 5.0, warnMax: 14.0, alarmMin: 3.0, alarmMax: 16.0, level: '严重', notifyMethod: '系统消息,短信,邮件', enabled: '启用' },
  { id: 4, parameter: 'ammoniaNitrogen', paramLabel: '氨氮', unit: 'mg/L', scene: '全部场景', normalMin: 0, normalMax: 0.2, warnMin: 0, warnMax: 0.3, alarmMin: 0, alarmMax: 0.5, level: '严重', notifyMethod: '系统消息,短信', enabled: '启用' },
  { id: 5, parameter: 'turbidity', paramLabel: '浑浊度', unit: 'NTU', scene: '全部场景', normalMin: 0, normalMax: 40, warnMin: 0, warnMax: 60, alarmMin: 0, alarmMax: 100, level: '一般', notifyMethod: '系统消息', enabled: '启用' },
  { id: 6, parameter: 'nitrite', paramLabel: '亚硝酸盐', unit: 'mg/L', scene: '草鱼养殖', normalMin: 0, normalMax: 0.1, warnMin: 0, warnMax: 0.15, alarmMin: 0, alarmMax: 0.2, level: '重要', notifyMethod: '系统消息,短信', enabled: '启用' },
  { id: 7, parameter: 'temperature', paramLabel: '水温', unit: '°C', scene: '南美白对虾', normalMin: 22, normalMax: 30, warnMin: 20, warnMax: 32, alarmMin: 16, alarmMax: 36, level: '严重', notifyMethod: '系统消息,短信,邮件', enabled: '禁用' },
])

const searchForm = reactive({ parameter: '', scene: '', enabled: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.parameter && row.parameter !== searchForm.parameter) return false
    if (searchForm.scene && !row.scene.includes(searchForm.scene)) return false
    if (searchForm.enabled && row.enabled !== searchForm.enabled) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.parameter = ''; searchForm.scene = ''; searchForm.enabled = '' }

// 弹窗
const dialogVisible = ref(false)
const dialogTitle = ref('新增报警设置')
const formRef = ref(null)
let editId = null
const form = reactive({
  parameter: '', unit: '', scene: '全部场景',
  normalMin: 0, normalMax: 100, warnMin: 0, warnMax: 110, alarmMin: 0, alarmMax: 120,
  level: '重要', notifyMethods: ['系统消息'], enabled: '启用'
})

const rules = {
  parameter: [{ required: true, message: '请选择监测参数', trigger: 'change' }],
  scene: [{ required: true, message: '请输入应用场景', trigger: 'blur' }]
}

const fillUnit = (val) => {
  const opt = parameterOptions.find(p => p.value === val)
  if (opt) form.unit = opt.unit
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { parameter: '', unit: '', scene: '全部场景', normalMin: 0, normalMax: 100, warnMin: 0, warnMax: 110, alarmMin: 0, alarmMax: 120, level: '重要', notifyMethods: ['系统消息'], enabled: '启用' })
  dialogTitle.value = '新增报警设置'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row, notifyMethods: row.notifyMethod ? row.notifyMethod.split(',') : ['系统消息'] })
  dialogTitle.value = '编辑报警设置'
  dialogVisible.value = true
}

const submitForm = () => {
  formRef.value?.validate(valid => {
    if (!valid) return
    const paramOpt = parameterOptions.find(p => p.value === form.parameter)
    const saveData = { ...form, paramLabel: paramOpt?.label || form.parameter, notifyMethod: form.notifyMethods.join(',') }
    if (editId) {
      const idx = tableData.value.findIndex(r => r.id === editId)
      if (idx !== -1) tableData.value[idx] = { ...tableData.value[idx], ...saveData }
      ElMessage.success('编辑成功')
    } else {
      tableData.value.unshift({ id: Date.now(), ...saveData })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除该报警设置？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const toggleEnabled = (row, val) => {
  row.enabled = val ? '启用' : '禁用'
  ElMessage.success(`报警规则已${row.enabled}`)
}
</script>

<style scoped>
.alarm-setting {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
.range-text { font-weight: 600; color: #67c23a; }
.range-text.warn { color: #e6a23c; }
.range-text.error { color: #f56c6c; }
</style>

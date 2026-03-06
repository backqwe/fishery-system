<template>
  <div class="equipment-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">设备管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增设备
          </el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="设备类型">
            <el-select v-model="searchForm.type" placeholder="全部类型" clearable style="width:140px">
              <el-option v-for="t in typeOptions" :key="t" :label="t" :value="t" />
            </el-select>
          </el-form-item>
          <el-form-item label="设备名称">
            <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:150px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:110px">
              <el-option label="运行中" value="运行中" />
              <el-option label="停止" value="停止" />
              <el-option label="故障" value="故障" />
              <el-option label="维护中" value="维护中" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-table :data="filteredData" stripe border style="width:100%">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="code" label="设备编号" width="120" />
        <el-table-column prop="name" label="设备名称" min-width="140" />
        <el-table-column prop="type" label="设备类型" width="120" />
        <el-table-column prop="model" label="设备型号" width="120" />
        <el-table-column prop="pondName" label="安装位置" min-width="120" />
        <el-table-column prop="manufacturer" label="厂商" width="120" />
        <el-table-column prop="installDate" label="安装日期" width="110" />
        <el-table-column prop="lastMaintain" label="上次维护" width="110" />
        <el-table-column prop="runHours" label="累计运行(h)" width="110" align="center" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '运行中' ? 'success' : row.status === '停止' ? 'info' : row.status === '故障' ? 'danger' : 'warning'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button :type="row.status === '运行中' ? 'warning' : 'success'" link size="small" @click="toggleRun(row)">
              {{ row.status === '运行中' ? '停止' : '启动' }}
            </el-button>
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="设备编号" prop="code">
          <el-input v-model="form.code" placeholder="如 EQ001" />
        </el-form-item>
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="form.type" style="width:100%">
            <el-option v-for="t in typeOptions" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
        <el-form-item label="设备型号" prop="model">
          <el-input v-model="form.model" placeholder="请输入设备型号" />
        </el-form-item>
        <el-form-item label="安装位置" prop="pondName">
          <el-input v-model="form.pondName" placeholder="如 1号池塘" />
        </el-form-item>
        <el-form-item label="生产厂商" prop="manufacturer">
          <el-input v-model="form.manufacturer" />
        </el-form-item>
        <el-form-item label="安装日期" prop="installDate">
          <el-date-picker v-model="form.installDate" type="date" value-format="YYYY-MM-DD" placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="运行状态" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="运行中" value="运行中" />
            <el-option label="停止" value="停止" />
            <el-option label="故障" value="故障" />
            <el-option label="维护中" value="维护中" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" />
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

// ===================== Mock 数据 =====================
const typeOptions = ['增氧机', '水质监测仪', '投饵机', '水泵', '过滤系统', '温控设备', '视频监控']

const tableData = ref([
  { id: 1, code: 'EQ001', name: '1号增氧机', type: '增氧机', model: 'YC-3000', pondName: '1号池塘', manufacturer: '湛江水产设备厂', installDate: '2021-04-15', lastMaintain: '2024-01-20', runHours: 8760, status: '运行中', remark: '' },
  { id: 2, code: 'EQ002', name: '2号增氧机', type: '增氧机', model: 'YC-3000', pondName: '2号池塘', manufacturer: '湛江水产设备厂', installDate: '2021-04-15', lastMaintain: '2024-01-20', runHours: 8620, status: '运行中', remark: '' },
  { id: 3, code: 'EQ003', name: '3号增氧机', type: '增氧机', model: 'YC-5000', pondName: '3号池塘', manufacturer: '湛江水产设备厂', installDate: '2021-05-01', lastMaintain: '2024-02-15', runHours: 7920, status: '故障', remark: '叶轮损坏，待维修' },
  { id: 4, code: 'EQ004', name: 'A区水质监测站', type: '水质监测仪', model: 'WQM-5000', pondName: 'A区域', manufacturer: '广州环境监测设备', installDate: '2022-01-10', lastMaintain: '2024-03-01', runHours: 17520, status: '运行中', remark: '' },
  { id: 5, code: 'EQ005', name: '1号自动投饵机', type: '投饵机', model: 'TL-200', pondName: '1号池塘', manufacturer: '珠海智能渔业', installDate: '2022-06-20', lastMaintain: '2024-02-01', runHours: 3650, status: '运行中', remark: '' },
  { id: 6, code: 'EQ006', name: '主循环水泵', type: '水泵', model: 'BT-150', pondName: '公共管道', manufacturer: '上海泵业集团', installDate: '2020-08-01', lastMaintain: '2023-12-10', runHours: 25920, status: '运行中', remark: '' },
  { id: 7, code: 'EQ007', name: 'B区增氧机', type: '增氧机', model: 'YC-3000', pondName: 'B区域', manufacturer: '湛江水产设备厂', installDate: '2021-06-01', lastMaintain: '2024-01-10', runHours: 8200, status: '维护中', remark: '定期保养中' },
  { id: 8, code: 'EQ008', name: '全场视频监控系统', type: '视频监控', model: 'HK-DS8632', pondName: '全场区域', manufacturer: '海康威视', installDate: '2023-03-15', lastMaintain: '2024-02-20', runHours: 8760, status: '运行中', remark: '' },
])

const searchForm = reactive({ type: '', name: '', status: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.type && row.type !== searchForm.type) return false
    if (searchForm.name && !row.name.includes(searchForm.name)) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.type = ''; searchForm.name = ''; searchForm.status = '' }

const dialogVisible = ref(false)
const dialogTitle = ref('新增设备')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', type: '增氧机', model: '', pondName: '', manufacturer: '', installDate: '', status: '运行中', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入设备编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入设备名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择设备类型', trigger: 'change' }]
}

const toggleRun = (row) => {
  if (row.status === '运行中') {
    row.status = '停止'
    ElMessage.warning(`${row.name} 已停止（Mock）`)
  } else {
    row.status = '运行中'
    ElMessage.success(`${row.name} 已启动（Mock）`)
  }
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', type: '增氧机', model: '', pondName: '', manufacturer: '', installDate: '', status: '运行中', remark: '' })
  dialogTitle.value = '新增设备'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑设备'
  dialogVisible.value = true
}

const submitForm = () => {
  formRef.value?.validate(valid => {
    if (!valid) return
    if (editId) {
      const idx = tableData.value.findIndex(r => r.id === editId)
      if (idx !== -1) tableData.value[idx] = { ...tableData.value[idx], ...form }
      ElMessage.success('编辑成功')
    } else {
      tableData.value.unshift({ id: Date.now(), runHours: 0, lastMaintain: '-', ...form })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除设备 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.equipment-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

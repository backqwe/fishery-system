<template>
  <div class="monitor-point-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">监测点管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增监测点
          </el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="所属池塘">
            <el-select v-model="searchForm.pondId" placeholder="全部池塘" clearable style="width:140px">
              <el-option v-for="p in pondOptions" :key="p.id" :label="p.name" :value="p.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="监测点名称">
            <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:150px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:110px">
              <el-option label="在线" value="在线" />
              <el-option label="离线" value="离线" />
              <el-option label="故障" value="故障" />
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
        <el-table-column prop="code" label="监测点编号" width="130" />
        <el-table-column prop="name" label="监测点名称" min-width="150" />
        <el-table-column prop="pondName" label="所属池塘" width="110" />
        <el-table-column prop="location" label="安装位置" min-width="120" />
        <el-table-column prop="depth" label="安装深度(m)" width="110" align="center" />
        <el-table-column prop="monitorItems" label="监测项目" min-width="180" show-overflow-tooltip />
        <el-table-column prop="deviceModel" label="设备型号" width="120" />
        <el-table-column prop="lastOnlineTime" label="最后在线时间" width="160" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '在线' ? 'success' : row.status === '离线' ? 'warning' : 'danger'" size="small">
              <el-icon v-if="row.status === '在线'" class="is-loading" style="font-size:10px"><Loading /></el-icon>
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="success" link size="small" @click="testConnect(row)">测试连接</el-button>
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
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="监测点编号" prop="code">
          <el-input v-model="form.code" placeholder="如 MP001" />
        </el-form-item>
        <el-form-item label="监测点名称" prop="name">
          <el-input v-model="form.name" placeholder="如 A区-1号监测点" />
        </el-form-item>
        <el-form-item label="所属池塘" prop="pondId">
          <el-select v-model="form.pondId" style="width:100%" @change="onPondChange">
            <el-option v-for="p in pondOptions" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="安装位置" prop="location">
          <el-select v-model="form.location" style="width:100%">
            <el-option label="水面" value="水面" />
            <el-option label="水中央" value="水中央" />
            <el-option label="水底" value="水底" />
            <el-option label="进水口" value="进水口" />
            <el-option label="出水口" value="出水口" />
          </el-select>
        </el-form-item>
        <el-form-item label="安装深度(m)" prop="depth">
          <el-input-number v-model="form.depth" :min="0" :max="5" :precision="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="监测项目" prop="monitorItems">
          <el-checkbox-group v-model="form.monitorItemsArr">
            <el-checkbox label="水温">水温</el-checkbox>
            <el-checkbox label="pH值">pH值</el-checkbox>
            <el-checkbox label="溶解氧">溶解氧</el-checkbox>
            <el-checkbox label="氨氮">氨氮</el-checkbox>
            <el-checkbox label="浑浊度">浑浊度</el-checkbox>
            <el-checkbox label="亚硝酸盐">亚硝酸盐</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="设备型号" prop="deviceModel">
          <el-input v-model="form.deviceModel" placeholder="如 WQM-5000" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="在线">在线</el-radio>
            <el-radio label="离线">离线</el-radio>
            <el-radio label="故障">故障</el-radio>
          </el-radio-group>
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
const pondOptions = [
  { id: 1, name: '1号池塘' }, { id: 2, name: '2号池塘' }, { id: 3, name: '3号池塘' },
  { id: 4, name: '4号池塘' }, { id: 5, name: '5号池塘' }, { id: 6, name: '6号池塘' },
  { id: 7, name: '7号池塘' }, { id: 8, name: '8号池塘' },
]

const tableData = ref([
  { id: 1, code: 'MP001', name: 'A区-1号监测点', pondId: 1, pondName: '1号池塘', location: '水中央', depth: 0.5, monitorItems: '水温,pH值,溶解氧,氨氮,浑浊度', deviceModel: 'WQM-5000', lastOnlineTime: '2024-03-06 15:30:05', status: '在线', remark: '' },
  { id: 2, code: 'MP002', name: 'A区-2号监测点', pondId: 2, pondName: '2号池塘', location: '水中央', depth: 0.5, monitorItems: '水温,pH值,溶解氧,氨氮', deviceModel: 'WQM-5000', lastOnlineTime: '2024-03-06 15:30:08', status: '在线', remark: '' },
  { id: 3, code: 'MP003', name: 'B区-1号监测点', pondId: 3, pondName: '3号池塘', location: '水中央', depth: 0.5, monitorItems: '水温,pH值,溶解氧,氨氮,浑浊度', deviceModel: 'WQM-3000', lastOnlineTime: '2024-03-06 15:30:10', status: '在线', remark: '预警中' },
  { id: 4, code: 'MP004', name: 'B区-2号监测点', pondId: 4, pondName: '4号池塘', location: '水中央', depth: 1.0, monitorItems: '水温,pH值,溶解氧,氨氮', deviceModel: 'WQM-3000', lastOnlineTime: '2024-03-06 15:30:12', status: '在线', remark: '' },
  { id: 5, code: 'MP005', name: 'C区-1号监测点', pondId: 6, pondName: '6号池塘', location: '进水口', depth: 0.3, monitorItems: '水温,溶解氧,氨氮', deviceModel: 'WQM-2000', lastOnlineTime: '2024-03-06 15:30:15', status: '在线', remark: '' },
  { id: 6, code: 'MP006', name: 'C区-2号监测点', pondId: 7, pondName: '7号池塘', location: '水中央', depth: 0.5, monitorItems: '水温,pH值,溶解氧,氨氮,浑浊度,亚硝酸盐', deviceModel: 'WQM-5000', lastOnlineTime: '2024-03-06 15:30:20', status: '在线', remark: '' },
  { id: 7, code: 'MP007', name: 'D区-1号监测点', pondId: 8, pondName: '8号池塘', location: '水底', depth: 1.5, monitorItems: '水温,pH值,溶解氧,氨氮', deviceModel: 'WQM-3000', lastOnlineTime: '2024-03-06 15:30:22', status: '在线', remark: '异常报警' },
  { id: 8, code: 'MP008', name: '备用监测点1', pondId: 5, pondName: '5号池塘', location: '水中央', depth: 0.5, monitorItems: '水温,溶解氧', deviceModel: 'WQM-1000', lastOnlineTime: '2024-03-05 10:15:00', status: '离线', remark: '设备维护中' },
])

const searchForm = reactive({ pondId: '', name: '', status: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.pondId && row.pondId !== searchForm.pondId) return false
    if (searchForm.name && !row.name.includes(searchForm.name)) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.pondId = ''; searchForm.name = ''; searchForm.status = '' }

const dialogVisible = ref(false)
const dialogTitle = ref('新增监测点')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', pondId: '', pondName: '', location: '水中央', depth: 0.5, monitorItemsArr: ['水温', 'pH值', '溶解氧', '氨氮'], deviceModel: '', status: '在线', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  pondId: [{ required: true, message: '请选择所属池塘', trigger: 'change' }]
}

const onPondChange = (val) => {
  const pond = pondOptions.find(p => p.id === val)
  form.pondName = pond?.name || ''
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', pondId: '', pondName: '', location: '水中央', depth: 0.5, monitorItemsArr: ['水温', 'pH值', '溶解氧', '氨氮'], deviceModel: '', status: '在线', remark: '' })
  dialogTitle.value = '新增监测点'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row, monitorItemsArr: row.monitorItems ? row.monitorItems.split(',') : [] })
  dialogTitle.value = '编辑监测点'
  dialogVisible.value = true
}

const testConnect = (row) => {
  ElMessage.success(`监测点 "${row.name}" 连接测试成功（Mock）`)
}

const submitForm = () => {
  formRef.value?.validate(valid => {
    if (!valid) return
    const saveData = { ...form, monitorItems: form.monitorItemsArr.join(',') }
    if (editId) {
      const idx = tableData.value.findIndex(r => r.id === editId)
      if (idx !== -1) tableData.value[idx] = { ...tableData.value[idx], ...saveData }
      ElMessage.success('编辑成功')
    } else {
      tableData.value.unshift({ id: Date.now(), lastOnlineTime: '-', ...saveData })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除监测点 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.monitor-point-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

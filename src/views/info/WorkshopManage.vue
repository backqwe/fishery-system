<template>
  <div class="workshop-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">车间管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增车间
          </el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="所属养殖场">
            <el-select v-model="searchForm.farmId" placeholder="全部养殖场" clearable style="width:160px">
              <el-option v-for="f in farmOptions" :key="f.id" :label="f.name" :value="f.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="车间名称">
            <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:160px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:110px">
              <el-option label="使用中" value="使用中" />
              <el-option label="维护中" value="维护中" />
              <el-option label="已停用" value="已停用" />
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
        <el-table-column prop="code" label="车间编码" width="120" />
        <el-table-column prop="name" label="车间名称" min-width="140" />
        <el-table-column prop="farmName" label="所属养殖场" min-width="140" />
        <el-table-column prop="type" label="车间类型" width="110" />
        <el-table-column prop="area" label="面积(㎡)" width="100" align="center" />
        <el-table-column prop="pondCount" label="池塘数量" width="90" align="center" />
        <el-table-column prop="manager" label="车间主管" width="90" />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '使用中' ? 'success' : row.status === '维护中' ? 'warning' : 'danger'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="120" />
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="540px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="车间编码" prop="code">
          <el-input v-model="form.code" placeholder="如 WS001" />
        </el-form-item>
        <el-form-item label="车间名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入车间名称" />
        </el-form-item>
        <el-form-item label="所属养殖场" prop="farmId">
          <el-select v-model="form.farmId" style="width:100%" @change="onFarmChange">
            <el-option v-for="f in farmOptions" :key="f.id" :label="f.name" :value="f.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="车间类型" prop="type">
          <el-select v-model="form.type" style="width:100%">
            <el-option label="室内养殖车间" value="室内养殖车间" />
            <el-option label="室外养殖区" value="室外养殖区" />
            <el-option label="孵化车间" value="孵化车间" />
            <el-option label="暂养车间" value="暂养车间" />
          </el-select>
        </el-form-item>
        <el-form-item label="面积(㎡)" prop="area">
          <el-input-number v-model="form.area" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="车间主管" prop="manager">
          <el-input v-model="form.manager" placeholder="请输入车间主管姓名" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="使用中" value="使用中" />
            <el-option label="维护中" value="维护中" />
            <el-option label="已停用" value="已停用" />
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
const farmOptions = [
  { id: 1, name: '第一养殖场' },
  { id: 2, name: '第二养殖场' },
  { id: 3, name: '第三养殖场' },
]

const tableData = ref([
  { id: 1, code: 'WS001', name: 'A区养殖车间', farmId: 1, farmName: '第一养殖场', type: '室外养殖区', area: 8500, pondCount: 10, manager: '张三', status: '使用中', createTime: '2020-04-01', remark: '' },
  { id: 2, code: 'WS002', name: 'B区养殖车间', farmId: 1, farmName: '第一养殖场', type: '室外养殖区', area: 7200, pondCount: 8, manager: '李四', status: '使用中', createTime: '2020-04-01', remark: '' },
  { id: 3, code: 'WS003', name: 'C区孵化车间', farmId: 1, farmName: '第一养殖场', type: '孵化车间', area: 2800, pondCount: 4, manager: '王五', status: '使用中', createTime: '2021-02-15', remark: '' },
  { id: 4, code: 'WS004', name: 'A区对虾车间', farmId: 2, farmName: '第二养殖场', type: '室内养殖车间', area: 5600, pondCount: 6, manager: '赵六', status: '使用中', createTime: '2021-07-01', remark: '对虾精养区' },
  { id: 5, code: 'WS005', name: 'B区暂养车间', farmId: 2, farmName: '第二养殖场', type: '暂养车间', area: 1200, pondCount: 4, manager: '钱七', status: '维护中', createTime: '2022-03-20', remark: '' },
  { id: 6, code: 'WS006', name: '东区养殖车间', farmId: 3, farmName: '第三养殖场', type: '室外养殖区', area: 9800, pondCount: 10, manager: '孙八', status: '已停用', createTime: '2022-02-01', remark: '停产整改中' },
])

const searchForm = reactive({ farmId: '', name: '', status: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.farmId && row.farmId !== searchForm.farmId) return false
    if (searchForm.name && !row.name.includes(searchForm.name)) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.farmId = ''; searchForm.name = ''; searchForm.status = '' }

const dialogVisible = ref(false)
const dialogTitle = ref('新增车间')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', farmId: '', farmName: '', type: '室外养殖区', area: 5000, manager: '', status: '使用中', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入车间编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入车间名称', trigger: 'blur' }],
  farmId: [{ required: true, message: '请选择所属养殖场', trigger: 'change' }]
}

const onFarmChange = (val) => {
  const farm = farmOptions.find(f => f.id === val)
  form.farmName = farm?.name || ''
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', farmId: '', farmName: '', type: '室外养殖区', area: 5000, manager: '', status: '使用中', remark: '' })
  dialogTitle.value = '新增车间'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑车间'
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
      tableData.value.unshift({ id: Date.now(), pondCount: 0, createTime: new Date().toLocaleDateString('zh-CN').replace(/\//g,'-'), ...form })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除车间 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.workshop-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

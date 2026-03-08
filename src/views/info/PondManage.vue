<template>
  <div class="pond-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">池塘管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增池塘
          </el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="所属车间">
            <el-select v-model="searchForm.workshopId" placeholder="全部车间" clearable style="width:150px">
              <el-option v-for="w in workshopOptions" :key="w.id" :label="w.name" :value="w.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="池塘名称">
            <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:150px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:110px">
              <el-option label="正常" value="正常" />
              <el-option label="预警" value="预警" />
              <el-option label="维护" value="维护" />
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
        <el-table-column prop="code" label="池塘编号" width="110" />
        <el-table-column prop="name" label="池塘名称" min-width="120" />
        <el-table-column prop="workshopName" label="所属车间" min-width="130" />
        <el-table-column prop="area" label="面积(亩)" width="90" align="center" />
        <el-table-column prop="depth" label="水深(m)" width="85" align="center" />
        <el-table-column prop="type" label="养殖类型" width="110" />
        <el-table-column prop="currentSpecies" label="当前养殖品种" min-width="120" />
        <el-table-column prop="fishCount" label="放养数量(尾)" width="120" align="center" />
        <el-table-column prop="manager" label="负责人" width="85" />
        <el-table-column prop="status" label="状态" width="85" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '正常' ? 'success' : row.status === '预警' ? 'warning' : 'info'" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
            <el-button type="warning" link size="small" @click="openEditDialog(row)">编辑</el-button>
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="池塘编号" prop="code">
          <el-input v-model="form.code" placeholder="如 POND001" />
        </el-form-item>
        <el-form-item label="池塘名称" prop="name">
          <el-input v-model="form.name" placeholder="如 1号池塘" />
        </el-form-item>
        <el-form-item label="所属车间" prop="workshopId">
          <el-select v-model="form.workshopId" style="width:100%" @change="onWorkshopChange">
            <el-option v-for="w in workshopOptions" :key="w.id" :label="w.name" :value="w.id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="面积(亩)" prop="area">
              <el-input-number v-model="form.area" :min="0.1" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="水深(m)" prop="depth">
              <el-input-number v-model="form.depth" :min="0.5" :precision="1" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="养殖类型" prop="type">
          <el-select v-model="form.type" style="width:100%">
            <el-option label="草鱼塘" value="草鱼塘" />
            <el-option label="鲤鱼塘" value="鲤鱼塘" />
            <el-option label="鲫鱼塘" value="鲫鱼塘" />
            <el-option label="鲈鱼塘" value="鲈鱼塘" />
            <el-option label="对虾池" value="对虾池" />
            <el-option label="混养塘" value="混养塘" />
          </el-select>
        </el-form-item>
        <el-form-item label="当前养殖品种" prop="currentSpecies">
          <el-input v-model="form.currentSpecies" placeholder="如 草鱼" />
        </el-form-item>
        <el-form-item label="放养数量(尾)" prop="fishCount">
          <el-input-number v-model="form.fishCount" :min="0" style="width:100%" />
        </el-form-item>
        <el-form-item label="负责人" prop="manager">
          <el-input v-model="form.manager" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="维护" value="维护" />
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
const workshopOptions = [
  { id: 1, name: 'A区养殖车间' },
  { id: 2, name: 'B区养殖车间' },
  { id: 3, name: 'C区孵化车间' },
  { id: 4, name: 'A区对虾车间' },
  { id: 5, name: 'B区暂养车间' },
]

const tableData = ref([
  { id: 1, code: 'POND001', name: '1号池塘', workshopId: 1, workshopName: 'A区养殖车间', area: 5.2, depth: 2.5, type: '草鱼塘', currentSpecies: '草鱼', fishCount: 3200, manager: '张三', status: '正常', createTime: '2020-04-10', remark: '' },
  { id: 2, code: 'POND002', name: '2号池塘', workshopId: 1, workshopName: 'A区养殖车间', area: 8.0, depth: 3.0, type: '鲤鱼塘', currentSpecies: '鲤鱼', fishCount: 5000, manager: '李四', status: '正常', createTime: '2020-04-10', remark: '' },
  { id: 3, code: 'POND003', name: '3号池塘', workshopId: 2, workshopName: 'B区养殖车间', area: 4.5, depth: 2.0, type: '鲫鱼塘', currentSpecies: '鲫鱼', fishCount: 2800, manager: '王五', status: '预警', createTime: '2020-04-15', remark: '水质预警' },
  { id: 4, code: 'POND004', name: '4号池塘', workshopId: 2, workshopName: 'B区养殖车间', area: 10.0, depth: 3.5, type: '混养塘', currentSpecies: '草鱼+鲢鱼', fishCount: 6500, manager: '张三', status: '正常', createTime: '2020-05-01', remark: '' },
  { id: 5, code: 'POND005', name: '5号池塘', workshopId: 2, workshopName: 'B区养殖车间', area: 6.8, depth: 2.8, type: '草鱼塘', currentSpecies: '草鱼', fishCount: 4100, manager: '赵六', status: '维护', createTime: '2020-05-01', remark: '维护中' },
  { id: 6, code: 'POND006', name: '6号池塘', workshopId: 4, workshopName: 'A区对虾车间', area: 3.5, depth: 1.5, type: '对虾池', currentSpecies: '南美白对虾', fishCount: 85000, manager: '钱七', status: '正常', createTime: '2021-07-10', remark: '' },
  { id: 7, code: 'POND007', name: '7号池塘', workshopId: 4, workshopName: 'A区对虾车间', area: 4.2, depth: 1.8, type: '对虾池', currentSpecies: '南美白对虾', fishCount: 92000, manager: '钱七', status: '正常', createTime: '2021-07-10', remark: '' },
  { id: 8, code: 'POND008', name: '8号池塘', workshopId: 1, workshopName: 'A区养殖车间', area: 7.3, depth: 3.2, type: '鲈鱼塘', currentSpecies: '鲈鱼', fishCount: 3800, manager: '孙八', status: '预警', createTime: '2021-09-01', remark: '溶氧偏低' },
])

const searchForm = reactive({ workshopId: '', name: '', status: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.workshopId && row.workshopId !== searchForm.workshopId) return false
    if (searchForm.name && !row.name.includes(searchForm.name)) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.workshopId = ''; searchForm.name = ''; searchForm.status = '' }

const dialogVisible = ref(false)
const dialogTitle = ref('新增池塘')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', workshopId: '', workshopName: '', area: 5.0, depth: 2.5, type: '草鱼塘', currentSpecies: '', fishCount: 0, manager: '', status: '正常', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入池塘编号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入池塘名称', trigger: 'blur' }],
  workshopId: [{ required: true, message: '请选择所属车间', trigger: 'change' }]
}

const onWorkshopChange = (val) => {
  const ws = workshopOptions.find(w => w.id === val)
  form.workshopName = ws?.name || ''
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', workshopId: '', workshopName: '', area: 5.0, depth: 2.5, type: '草鱼塘', currentSpecies: '', fishCount: 0, manager: '', status: '正常', remark: '' })
  dialogTitle.value = '新增池塘'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑池塘'
  dialogVisible.value = true
}

const viewDetail = (row) => {
  ElMessage.info(`查看 ${row.name} 详情（可跳转到详情页）`)
}

const submitForm = () => {
  formRef.value?.validate(valid => {
    if (!valid) return
    if (editId) {
      const idx = tableData.value.findIndex(r => r.id === editId)
      if (idx !== -1) tableData.value[idx] = { ...tableData.value[idx], ...form }
      ElMessage.success('编辑成功')
    } else {
      tableData.value.unshift({ id: Date.now(), createTime: new Date().toLocaleDateString('zh-CN').replace(/\//g,'-'), ...form })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除池塘 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.pond-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

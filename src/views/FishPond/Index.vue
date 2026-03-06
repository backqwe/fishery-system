<template>
  <div>
    <div class="page-title">鱼塘管理</div>

    <!-- Search Bar -->
    <el-card shadow="hover" class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="鱼塘名称">
          <el-input v-model="searchForm.name" placeholder="请输入鱼塘名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="维护" value="维护" />
            <el-option label="空置" value="空置" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- Table -->
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>鱼塘列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon> 新增鱼塘
          </el-button>
        </div>
      </template>

      <el-table :data="pagedData" stripe v-loading="loading">
        <el-table-column prop="id" label="编号" width="60" />
        <el-table-column prop="name" label="鱼塘名称" width="120" />
        <el-table-column prop="area" label="面积(亩)" width="100" />
        <el-table-column prop="depth" label="水深(m)" width="100" />
        <el-table-column prop="type" label="类型" width="80" />
        <el-table-column prop="species" label="养殖品种" width="100" />
        <el-table-column prop="createTime" label="创建时间" width="120" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="180">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">详情</el-button>
            <el-button type="warning" link size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="filteredData.length"
        :page-sizes="[5, 10, 20]"
        layout="total, sizes, prev, pager, next"
        class="pagination"
      />
    </el-card>

    <!-- Add/Edit Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="鱼塘名称" prop="name">
              <el-input v-model="form.name" placeholder="请输入鱼塘名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="面积(亩)" prop="area">
              <el-input-number v-model="form.area" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="水深(m)" prop="depth">
              <el-input-number v-model="form.depth" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-select v-model="form.type">
                <el-option label="淡水" value="淡水" />
                <el-option label="海水" value="海水" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="养殖品种" prop="species">
              <el-input v-model="form.species" placeholder="请输入养殖品种" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status">
                <el-option label="正常" value="正常" />
                <el-option label="预警" value="预警" />
                <el-option label="维护" value="维护" />
                <el-option label="空置" value="空置" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fishPondList } from '@/mock/fishpond'

const router = useRouter()
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()

const searchForm = reactive({ name: '', status: '' })
const form = reactive({ id: 0, name: '', area: 0, depth: 0, type: '淡水', species: '', status: '正常' })
const rules = {
  name: [{ required: true, message: '请输入鱼塘名称', trigger: 'blur' }],
  area: [{ required: true, message: '请输入面积', trigger: 'blur' }]
}

const tableData = ref([...fishPondList])

const filteredData = computed(() => {
  return tableData.value.filter(item => {
    const nameMatch = !searchForm.name || item.name.includes(searchForm.name)
    const statusMatch = !searchForm.status || item.status === searchForm.status
    return nameMatch && statusMatch
  })
})

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const statusType = (status: string) => {
  const map: Record<string, string> = { '正常': 'success', '预警': 'warning', '维护': 'info', '空置': '' }
  return map[status] || ''
}

const handleSearch = () => { currentPage.value = 1 }
const resetSearch = () => { searchForm.name = ''; searchForm.status = ''; currentPage.value = 1 }

const handleView = (row: any) => { router.push(`/fishpond/detail/${row.id}`) }

const handleAdd = () => {
  dialogTitle.value = '新增鱼塘'
  Object.assign(form, { id: 0, name: '', area: 0, depth: 0, type: '淡水', species: '', status: '正常' })
  dialogVisible.value = true
}

const handleEdit = (row: any) => {
  dialogTitle.value = '编辑鱼塘'
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

const handleDelete = (row: any) => {
  ElMessageBox.confirm(`确认删除 ${row.name}？`, '提示', { type: 'warning' }).then(() => {
    const index = tableData.value.findIndex(i => i.id === row.id)
    if (index > -1) tableData.value.splice(index, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const handleSubmit = async () => {
  await formRef.value?.validate()
  if (form.id === 0) {
    const newId = Math.max(...tableData.value.map(i => i.id)) + 1
    tableData.value.push({ ...form, id: newId, createTime: new Date().toISOString().slice(0, 10) })
    ElMessage.success('新增成功')
  } else {
    const index = tableData.value.findIndex(i => i.id === form.id)
    if (index > -1) Object.assign(tableData.value[index], { ...form })
    ElMessage.success('编辑成功')
  }
  dialogVisible.value = false
}
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.search-card { margin-bottom: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.pagination { margin-top: 16px; justify-content: flex-end; display: flex; }
</style>

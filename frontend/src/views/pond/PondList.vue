<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>鱼塘列表</span>
          <el-button type="primary" @click="openDialog()">
            <el-icon><Plus /></el-icon> 新增鱼塘
          </el-button>
        </div>
      </template>
      <el-form :inline="true" class="search-form">
        <el-form-item label="鱼塘名称">
          <el-input v-model="search" placeholder="请输入鱼塘名称" clearable style="width:200px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="statusFilter" placeholder="全部" clearable style="width:120px">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="异常" value="异常" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="pagedData" stripe border>
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="name" label="鱼塘名称" />
        <el-table-column prop="area" label="面积(亩)" width="100" />
        <el-table-column prop="depth" label="深度(m)" width="100" />
        <el-table-column prop="species" label="养殖品种" />
        <el-table-column prop="quantity" label="数量(条)" width="100" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" text size="small" @click="viewDetail(row)">详情</el-button>
            <el-button type="warning" text size="small" @click="openDialog(row)">编辑</el-button>
            <el-button type="danger" text size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        style="margin-top:16px;justify-content:flex-end;display:flex"
        :total="filteredData.length"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="currentPage = $event"
        layout="total, prev, pager, next"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑鱼塘' : '新增鱼塘'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="鱼塘名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="面积(亩)"><el-input-number v-model="form.area" :min="0" :step="0.1" /></el-form-item>
        <el-form-item label="深度(m)"><el-input-number v-model="form.depth" :min="0" :step="0.1" /></el-form-item>
        <el-form-item label="位置"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="养殖品种">
          <el-select v-model="form.species">
            <el-option v-for="s in ['草鱼','鲤鱼','鲫鱼','鲢鱼','其他']" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="放养数量"><el-input-number v-model="form.quantity" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ponds as mockPonds } from '@/mock/pond.js'

const router = useRouter()
const tableData = ref([...mockPonds])
const search = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = 6
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = ref({ name: '', area: 0, depth: 0, location: '', species: '草鱼', quantity: 0 })

const filteredData = computed(() => tableData.value.filter(row =>
  (!search.value || row.name.includes(search.value)) &&
  (!statusFilter.value || row.status === statusFilter.value)
))

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredData.value.slice(start, start + pageSize)
})

const statusType = (s) => s === '正常' ? 'success' : s === '预警' ? 'warning' : 'danger'

const handleSearch = () => { currentPage.value = 1 }
const handleReset = () => { search.value = ''; statusFilter.value = ''; currentPage.value = 1 }

const openDialog = (row = null) => {
  isEdit.value = !!row
  form.value = row ? { ...row } : { name: '', area: 0, depth: 0, location: '', species: '草鱼', quantity: 0 }
  dialogVisible.value = true
}

const handleSave = () => {
  if (isEdit.value) {
    const idx = tableData.value.findIndex(r => r.id === form.value.id)
    if (idx !== -1) tableData.value[idx] = { ...form.value }
  } else {
    tableData.value.unshift({ ...form.value, id: Date.now(), status: '正常', createTime: new Date().toISOString().slice(0, 10) })
  }
  dialogVisible.value = false
  ElMessage.success('保存成功')
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确认删除 ${row.name}？`, '提示', { type: 'warning' })
    .then(() => {
      tableData.value = tableData.value.filter(r => r.id !== row.id)
      ElMessage.success('删除成功')
    })
}

const viewDetail = (row) => router.push(`/pond/detail/${row.id}`)
</script>

<style scoped>
.search-form { margin-bottom: 16px; }
</style>

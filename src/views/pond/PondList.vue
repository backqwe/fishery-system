<template>
  <div class="pond-list">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">鱼塘列表</span>
          <el-button type="primary" @click="$router.push('/pond/add')">
            <el-icon><Plus /></el-icon>新增鱼塘
          </el-button>
        </div>
      </template>

      <!-- 搜索区 -->
      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="鱼塘名称">
          <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:180px" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:120px">
            <el-option label="正常" value="正常" />
            <el-option label="预警" value="预警" />
            <el-option label="维护" value="维护" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="searchForm.type" placeholder="全部" clearable style="width:140px">
            <el-option label="草鱼塘" value="草鱼塘" />
            <el-option label="鲤鱼塘" value="鲤鱼塘" />
            <el-option label="鲫鱼塘" value="鲫鱼塘" />
            <el-option label="鲈鱼塘" value="鲈鱼塘" />
            <el-option label="鲢鱼塘" value="鲢鱼塘" />
            <el-option label="混养塘" value="混养塘" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="pagedData" stripe border style="width:100%">
        <el-table-column prop="id" label="编号" width="70" align="center" />
        <el-table-column prop="name" label="鱼塘名称" min-width="110" />
        <el-table-column prop="area" label="面积(亩)" width="100" align="center" />
        <el-table-column prop="depth" label="水深(m)" width="90" align="center" />
        <el-table-column prop="type" label="类型" width="100" align="center" />
        <el-table-column prop="location" label="位置" min-width="110" />
        <el-table-column prop="fishCount" label="存塘数量" width="100" align="center" />
        <el-table-column prop="manager" label="负责人" width="90" align="center" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewDetail(row)">详情</el-button>
            <el-button type="warning" link size="small" @click="editPond(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deletePond(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="filteredData.length"
          :page-sizes="[5, 10, 20]"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ponds } from '@/mock/pond.js'

const router = useRouter()

const searchForm = ref({ name: '', status: '', type: '' })
const currentPage = ref(1)
const pageSize = ref(10)
const tableData = ref([...ponds])

const filteredData = computed(() => {
  return tableData.value.filter(item => {
    const nameMatch = !searchForm.value.name || item.name.includes(searchForm.value.name)
    const statusMatch = !searchForm.value.status || item.status === searchForm.value.status
    const typeMatch = !searchForm.value.type || item.type === searchForm.value.type
    return nameMatch && statusMatch && typeMatch
  })
})

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const statusTagType = (status) => {
  const map = { 正常: 'success', 预警: 'warning', 维护: 'info' }
  return map[status] || 'info'
}

const handleSearch = () => { currentPage.value = 1 }
const handleReset = () => {
  searchForm.value = { name: '', status: '', type: '' }
  currentPage.value = 1
}

const viewDetail = (row) => router.push(`/pond/detail/${row.id}`)
const editPond = (row) => ElMessage.info(`编辑鱼塘: ${row.name}（功能演示）`)
const deletePond = (row) => {
  ElMessageBox.confirm(`确定删除鱼塘「${row.name}」吗？`, '提示', {
    type: 'warning'
  }).then(() => {
    const idx = tableData.value.findIndex(p => p.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  font-size: 16px;
  font-weight: 600;
}
.search-form {
  margin-bottom: 16px;
}
.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>

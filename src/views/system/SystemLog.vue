<template>
  <div class="system-log">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">系统日志</span>
          <el-button type="danger" plain @click="handleClear">清空日志</el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="操作用户">
          <el-input v-model="searchForm.user" placeholder="请输入用户名" clearable style="width:140px" />
        </el-form-item>
        <el-form-item label="模块">
          <el-select v-model="searchForm.module" placeholder="全部" clearable style="width:130px">
            <el-option label="系统" value="系统" />
            <el-option label="鱼塘管理" value="鱼塘管理" />
            <el-option label="投喂记录" value="投喂记录" />
            <el-option label="水质监测" value="水质监测" />
            <el-option label="预警阈值" value="预警阈值" />
            <el-option label="养殖批次" value="养殖批次" />
          </el-select>
        </el-form-item>
        <el-form-item label="结果">
          <el-select v-model="searchForm.result" placeholder="全部" clearable style="width:100px">
            <el-option label="成功" value="成功" />
            <el-option label="失败" value="失败" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="pagedData" stripe border style="width:100%">
        <el-table-column prop="time" label="操作时间" width="175" />
        <el-table-column prop="user" label="操作用户" width="100" />
        <el-table-column prop="module" label="功能模块" width="110" />
        <el-table-column prop="action" label="操作类型" width="90" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.action === '登录' ? 'primary' : row.action === '新增' ? 'success' : row.action === '删除' ? 'danger' : 'info'"
              size="small"
            >{{ row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作详情" min-width="200" show-overflow-tooltip />
        <el-table-column prop="ip" label="IP地址" width="140" />
        <el-table-column prop="result" label="结果" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.result === '成功' ? 'success' : 'danger'" size="small">{{ row.result }}</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="filteredData.length"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { systemLogs } from '@/mock/system.js'

const logs = ref([...systemLogs])
const searchForm = ref({ user: '', module: '', result: '' })
const currentPage = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => logs.value.filter(l => {
  const userMatch = !searchForm.value.user || l.user.includes(searchForm.value.user)
  const moduleMatch = !searchForm.value.module || l.module === searchForm.value.module
  const resultMatch = !searchForm.value.result || l.result === searchForm.value.result
  return userMatch && moduleMatch && resultMatch
}))

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredData.value.slice(start, start + pageSize.value)
})

const handleSearch = () => { currentPage.value = 1 }
const handleReset = () => { searchForm.value = { user: '', module: '', result: '' }; currentPage.value = 1 }

const handleClear = () => {
  ElMessageBox.confirm('确定清空所有系统日志吗？', '警告', { type: 'warning' }).then(() => {
    logs.value = []
    ElMessage.success('日志已清空')
  }).catch(() => {})
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
.search-form { margin-bottom: 16px; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>

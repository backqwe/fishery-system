<template>
  <div class="feed-record">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">投喂记录</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>添加记录
          </el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-form :model="searchForm" inline class="search-form">
        <el-form-item label="鱼塘">
          <el-select v-model="searchForm.pondName" placeholder="全部" clearable style="width:130px">
            <el-option v-for="p in pondOptions" :key="p" :label="p" :value="p" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="searchForm.date" type="date" placeholder="选择日期" clearable value-format="YYYY-MM-DD" style="width:155px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="filteredData" stripe border style="width:100%">
        <el-table-column prop="date" label="日期" width="110" align="center" />
        <el-table-column prop="pondName" label="鱼塘" width="100" />
        <el-table-column prop="batchNo" label="批次号" min-width="140" />
        <el-table-column prop="feedType" label="饲料类型" width="110" />
        <el-table-column prop="amount" label="投喂量" width="90" align="center">
          <template #default="{ row }">{{ row.amount }} {{ row.unit }}</template>
        </el-table-column>
        <el-table-column prop="feedTime" label="投喂时间" width="100" align="center" />
        <el-table-column prop="operator" label="操作人" width="90" align="center" />
        <el-table-column prop="remark" label="备注" min-width="140" show-overflow-tooltip />
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="10"
          :total="filteredData.length"
          layout="total, prev, pager, next"
          background
        />
      </div>
    </el-card>

    <!-- 添加记录对话框 -->
    <el-dialog v-model="showAddDialog" title="添加投喂记录" width="500px">
      <el-form :model="addForm" label-width="100px" ref="addFormRef">
        <el-form-item label="鱼塘" prop="pondName" :rules="[{ required: true, message: '请选择鱼塘' }]">
          <el-select v-model="addForm.pondName" placeholder="请选择" style="width:100%">
            <el-option v-for="p in pondOptions" :key="p" :label="p" :value="p" />
          </el-select>
        </el-form-item>
        <el-form-item label="饲料类型">
          <el-select v-model="addForm.feedType" style="width:100%">
            <el-option label="颗粒饲料" value="颗粒饲料" />
            <el-option label="鲜活饵料" value="鲜活饵料" />
            <el-option label="绿藻" value="绿藻" />
            <el-option label="人工配合饲料" value="人工配合饲料" />
          </el-select>
        </el-form-item>
        <el-form-item label="投喂量(kg)">
          <el-input-number v-model="addForm.amount" :min="0.1" :precision="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="投喂时间">
          <el-time-picker v-model="addForm.feedTime" format="HH:mm" value-format="HH:mm" style="width:100%" />
        </el-form-item>
        <el-form-item label="操作人">
          <el-select v-model="addForm.operator" style="width:100%">
            <el-option label="张三" value="张三" />
            <el-option label="李四" value="李四" />
            <el-option label="王五" value="王五" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="addForm.remark" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { feedRecords } from '@/mock/aquaculture.js'

const records = ref([...feedRecords])
const showAddDialog = ref(false)
const addFormRef = ref(null)
const currentPage = ref(1)
const searchForm = ref({ pondName: '', date: '' })
const pondOptions = ['1号鱼塘', '2号鱼塘', '3号鱼塘', '4号鱼塘', '6号鱼塘']
const addForm = ref({ pondName: '', feedType: '颗粒饲料', amount: 50, feedTime: '08:00', operator: '张三', remark: '' })

const filteredData = computed(() => {
  return records.value.filter(r => {
    const pondMatch = !searchForm.value.pondName || r.pondName === searchForm.value.pondName
    const dateMatch = !searchForm.value.date || r.date === searchForm.value.date
    return pondMatch && dateMatch
  })
})

const handleSearch = () => { currentPage.value = 1 }
const handleReset = () => { searchForm.value = { pondName: '', date: '' }; currentPage.value = 1 }

const handleAdd = async () => {
  await addFormRef.value.validate()
  const today = new Date().toISOString().slice(0, 10)
  records.value.unshift({
    id: Date.now(),
    date: today,
    batchNo: 'PC202401001',
    unit: 'kg',
    ...addForm.value
  })
  showAddDialog.value = false
  ElMessage.success('投喂记录添加成功')
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
.search-form { margin-bottom: 16px; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>

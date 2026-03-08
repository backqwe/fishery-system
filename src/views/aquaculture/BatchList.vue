<template>
  <div class="batch-list">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">养殖批次</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>新建批次
          </el-button>
        </div>
      </template>

      <el-table :data="batches" stripe border style="width:100%">
        <el-table-column prop="batchNo" label="批次号" min-width="140" />
        <el-table-column prop="pondName" label="鱼塘" width="110" />
        <el-table-column prop="species" label="养殖品种" width="100" />
        <el-table-column prop="quantity" label="放养数量(尾)" width="120" align="center" />
        <el-table-column prop="weight" label="初始体重(kg)" width="120" align="center" />
        <el-table-column prop="startDate" label="开始日期" width="110" align="center" />
        <el-table-column prop="expectedEndDate" label="预计出塘" width="110" align="center" />
        <el-table-column prop="manager" label="负责人" width="90" align="center" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '养殖中' ? 'success' : 'info'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="viewBatch(row)">查看</el-button>
            <el-button v-if="row.status === '养殖中'" type="warning" link size="small" @click="markDone(row)">出塘</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建批次对话框 -->
    <el-dialog v-model="showAddDialog" title="新建养殖批次" width="560px">
      <el-form :model="addForm" label-width="110px" :rules="addRules" ref="addFormRef">
        <el-form-item label="鱼塘" prop="pondName">
          <el-select v-model="addForm.pondName" placeholder="请选择鱼塘" style="width:100%">
            <el-option v-for="p in pondOptions" :key="p" :label="p" :value="p" />
          </el-select>
        </el-form-item>
        <el-form-item label="养殖品种" prop="species">
          <el-input v-model="addForm.species" placeholder="如：草鱼" />
        </el-form-item>
        <el-form-item label="放养数量(尾)" prop="quantity">
          <el-input-number v-model="addForm.quantity" :min="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="初始体重(kg)" prop="weight">
          <el-input-number v-model="addForm.weight" :min="0.01" :precision="2" style="width:100%" />
        </el-form-item>
        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker v-model="addForm.startDate" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="预计出塘" prop="expectedEndDate">
          <el-date-picker v-model="addForm.expectedEndDate" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="负责人" prop="manager">
          <el-select v-model="addForm.manager" placeholder="请选择负责人" style="width:100%">
            <el-option label="张三" value="张三" />
            <el-option label="李四" value="李四" />
            <el-option label="王五" value="王五" />
            <el-option label="赵六" value="赵六" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAddBatch">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { batches as mockBatches } from '@/mock/aquaculture.js'

const batches = ref([...mockBatches])
const showAddDialog = ref(false)
const addFormRef = ref(null)

const pondOptions = ['1号鱼塘', '2号鱼塘', '3号鱼塘', '4号鱼塘', '6号鱼塘', '7号鱼塘']

const addForm = ref({
  pondName: '', species: '', quantity: 1000, weight: 0.05,
  startDate: '', expectedEndDate: '', manager: ''
})

const addRules = {
  pondName: [{ required: true, message: '请选择鱼塘', trigger: 'change' }],
  species: [{ required: true, message: '请输入品种', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  manager: [{ required: true, message: '请选择负责人', trigger: 'change' }]
}

const viewBatch = (row) => ElMessage.info(`查看批次 ${row.batchNo} 详情（功能演示）`)

const markDone = (row) => {
  row.status = '已出塘'
  ElMessage.success(`批次 ${row.batchNo} 已标记出塘`)
}

const handleAddBatch = async () => {
  await addFormRef.value.validate()
  const newBatch = {
    id: Date.now(),
    batchNo: `PC${new Date().getFullYear()}${String(Date.now()).slice(-5)}`,
    ...addForm.value,
    status: '养殖中'
  }
  batches.value.unshift(newBatch)
  showAddDialog.value = false
  ElMessage.success('养殖批次创建成功')
  addFormRef.value.resetFields()
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
</style>

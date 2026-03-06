<template>
  <div class="farm-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">养殖场管理</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增养殖场
          </el-button>
        </div>
      </template>

      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="养殖场名称">
            <el-input v-model="searchForm.name" placeholder="请输入名称" clearable style="width:180px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:120px">
              <el-option label="正常运营" value="正常运营" />
              <el-option label="停产维护" value="停产维护" />
              <el-option label="已注销" value="已注销" />
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
        <el-table-column prop="code" label="养殖场编码" width="130" />
        <el-table-column prop="name" label="养殖场名称" min-width="150" />
        <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="area" label="总面积(亩)" width="110" align="center" />
        <el-table-column prop="pondCount" label="池塘数量" width="90" align="center" />
        <el-table-column prop="manager" label="负责人" width="90" />
        <el-table-column prop="phone" label="联系电话" width="130" />
        <el-table-column prop="status" label="状态" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '正常运营' ? 'success' : row.status === '停产维护' ? 'warning' : 'danger'" size="small">
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

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="560px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="养殖场编码" prop="code">
          <el-input v-model="form.code" placeholder="如 FARM001" />
        </el-form-item>
        <el-form-item label="养殖场名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入养殖场名称" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>
        <el-form-item label="总面积(亩)" prop="area">
          <el-input-number v-model="form.area" :min="0" :precision="1" style="width:100%" />
        </el-form-item>
        <el-form-item label="负责人" prop="manager">
          <el-input v-model="form.manager" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="运营状态" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="正常运营" value="正常运营" />
            <el-option label="停产维护" value="停产维护" />
            <el-option label="已注销" value="已注销" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
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

// ===================== Mock 养殖场数据 =====================
const tableData = ref([
  { id: 1, code: 'FARM001', name: '第一养殖场', address: '广东省湛江市廉江市第一水产养殖基地', area: 320.5, pondCount: 28, manager: '张场长', phone: '13800138001', status: '正常运营', createTime: '2020-03-15', remark: '主要养殖草鱼、鲤鱼' },
  { id: 2, code: 'FARM002', name: '第二养殖场', address: '广东省湛江市廉江市第二水产养殖基地', area: 256.0, pondCount: 22, manager: '李场长', phone: '13800138002', status: '正常运营', createTime: '2021-06-01', remark: '主要养殖南美白对虾' },
  { id: 3, code: 'FARM003', name: '第三养殖场', address: '广东省湛江市雷州市龙门镇养殖区', area: 180.8, pondCount: 15, manager: '王场长', phone: '13800138003', status: '停产维护', createTime: '2022-01-10', remark: '设备更新中' },
])

const searchForm = reactive({ name: '', status: '' })
const page = ref(1)
const pageSize = ref(10)

const filteredData = computed(() => {
  return tableData.value.filter(row => {
    if (searchForm.name && !row.name.includes(searchForm.name)) return false
    if (searchForm.status && row.status !== searchForm.status) return false
    return true
  })
})

const handleSearch = () => { page.value = 1 }
const resetSearch = () => { searchForm.name = ''; searchForm.status = '' }

const dialogVisible = ref(false)
const dialogTitle = ref('新增养殖场')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', address: '', area: 100.0, manager: '', phone: '', status: '正常运营', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  manager: [{ required: true, message: '请输入负责人', trigger: 'blur' }]
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', address: '', area: 100.0, manager: '', phone: '', status: '正常运营', remark: '' })
  dialogTitle.value = '新增养殖场'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑养殖场'
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
  ElMessageBox.confirm(`确认删除养殖场 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.farm-manage {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

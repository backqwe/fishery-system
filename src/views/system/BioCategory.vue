<template>
  <div class="bio-category">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">生物类别设置</span>
          <el-button type="primary" @click="openAddDialog">
            <el-icon><Plus /></el-icon>新增类别
          </el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <div class="toolbar">
        <el-form inline :model="searchForm">
          <el-form-item label="类别名称">
            <el-input v-model="searchForm.name" placeholder="请输入类别名称" clearable style="width:180px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable style="width:120px">
              <el-option label="启用" value="启用" />
              <el-option label="禁用" value="禁用" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch"><el-icon><Search /></el-icon>查询</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 表格 -->
      <el-table :data="filteredData" stripe border style="width:100%">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="code" label="类别编码" width="120" />
        <el-table-column prop="name" label="类别名称" min-width="140" />
        <el-table-column prop="scientificName" label="学名" min-width="150" />
        <el-table-column prop="category" label="所属大类" width="120" />
        <el-table-column prop="habitat" label="适宜水温(°C)" width="130" align="center">
          <template #default="{ row }">{{ row.tempMin }}~{{ row.tempMax }}</template>
        </el-table-column>
        <el-table-column prop="phRange" label="适宜pH范围" width="120" align="center" />
        <el-table-column prop="growthPeriod" label="生长周期(月)" width="120" align="center" />
        <el-table-column prop="status" label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-switch
              :model-value="row.status === '启用'"
              @change="(val) => toggleStatus(row, val)"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="140" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link size="small" @click="deleteRow(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="540px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="110px">
        <el-form-item label="类别编码" prop="code">
          <el-input v-model="form.code" placeholder="如 FISH001" />
        </el-form-item>
        <el-form-item label="类别名称" prop="name">
          <el-input v-model="form.name" placeholder="如 草鱼" />
        </el-form-item>
        <el-form-item label="学名" prop="scientificName">
          <el-input v-model="form.scientificName" placeholder="拉丁文学名" />
        </el-form-item>
        <el-form-item label="所属大类" prop="category">
          <el-select v-model="form.category" placeholder="请选择" style="width:100%">
            <el-option label="淡水鱼类" value="淡水鱼类" />
            <el-option label="海水鱼类" value="海水鱼类" />
            <el-option label="甲壳类" value="甲壳类" />
            <el-option label="贝类" value="贝类" />
            <el-option label="藻类" value="藻类" />
          </el-select>
        </el-form-item>
        <el-row :gutter="12">
          <el-col :span="12">
            <el-form-item label="最低水温(°C)" prop="tempMin">
              <el-input-number v-model="form.tempMin" :min="0" :max="40" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最高水温(°C)" prop="tempMax">
              <el-input-number v-model="form.tempMax" :min="0" :max="40" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="pH范围" prop="phRange">
          <el-input v-model="form.phRange" placeholder="如 6.5~8.5" />
        </el-form-item>
        <el-form-item label="生长周期(月)" prop="growthPeriod">
          <el-input-number v-model="form.growthPeriod" :min="1" :max="36" style="width:100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio label="启用">启用</el-radio>
            <el-radio label="禁用">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="备注信息" />
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

// ===================== Mock 生物类别数据 =====================
const tableData = ref([
  { id: 1, code: 'FISH001', name: '草鱼', scientificName: 'Ctenopharyngodon idella', category: '淡水鱼类', tempMin: 15, tempMax: 32, phRange: '6.5~8.5', growthPeriod: 10, status: '启用', remark: '食草性鱼类，适应性强' },
  { id: 2, code: 'FISH002', name: '鲤鱼', scientificName: 'Cyprinus carpio', category: '淡水鱼类', tempMin: 10, tempMax: 35, phRange: '6.8~8.0', growthPeriod: 12, status: '启用', remark: '杂食性，耐低氧' },
  { id: 3, code: 'FISH003', name: '鲫鱼', scientificName: 'Carassius auratus', category: '淡水鱼类', tempMin: 5, tempMax: 30, phRange: '7.0~8.5', growthPeriod: 8, status: '启用', remark: '适应性极强' },
  { id: 4, code: 'FISH004', name: '鲈鱼', scientificName: 'Lateolabrax japonicus', category: '淡水鱼类', tempMin: 10, tempMax: 30, phRange: '6.5~8.0', growthPeriod: 14, status: '启用', remark: '肉质鲜美，经济价值高' },
  { id: 5, code: 'FISH005', name: '鲢鱼', scientificName: 'Hypophthalmichthys molitrix', category: '淡水鱼类', tempMin: 15, tempMax: 35, phRange: '7.0~8.5', growthPeriod: 12, status: '启用', remark: '滤食性，净化水质' },
  { id: 6, code: 'CRUST001', name: '南美白对虾', scientificName: 'Litopenaeus vannamei', category: '甲壳类', tempMin: 18, tempMax: 32, phRange: '7.5~8.5', growthPeriod: 4, status: '启用', remark: '生长快，市场需求大' },
  { id: 7, code: 'CRUST002', name: '中华绒螯蟹', scientificName: 'Eriocheir sinensis', category: '甲壳类', tempMin: 5, tempMax: 28, phRange: '7.0~8.5', growthPeriod: 18, status: '启用', remark: '俗称大闸蟹，高经济价值' },
  { id: 8, code: 'SHELL001', name: '牡蛎', scientificName: 'Crassostrea gigas', category: '贝类', tempMin: 5, tempMax: 30, phRange: '7.5~8.5', growthPeriod: 18, status: '禁用', remark: '海水养殖' },
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

// 弹窗
const dialogVisible = ref(false)
const dialogTitle = ref('新增生物类别')
const formRef = ref(null)
let editId = null
const form = reactive({ code: '', name: '', scientificName: '', category: '淡水鱼类', tempMin: 15, tempMax: 32, phRange: '6.5~8.5', growthPeriod: 10, status: '启用', remark: '' })

const rules = {
  code: [{ required: true, message: '请输入类别编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入类别名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择所属大类', trigger: 'change' }]
}

const openAddDialog = () => {
  editId = null
  Object.assign(form, { code: '', name: '', scientificName: '', category: '淡水鱼类', tempMin: 15, tempMax: 32, phRange: '6.5~8.5', growthPeriod: 10, status: '启用', remark: '' })
  dialogTitle.value = '新增生物类别'
  dialogVisible.value = true
}

const openEditDialog = (row) => {
  editId = row.id
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑生物类别'
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
      tableData.value.unshift({ id: Date.now(), ...form })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
  })
}

const deleteRow = (row) => {
  ElMessageBox.confirm(`确认删除类别 "${row.name}"？`, '提示', { type: 'warning' }).then(() => {
    const idx = tableData.value.findIndex(r => r.id === row.id)
    if (idx !== -1) tableData.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const toggleStatus = (row, val) => {
  row.status = val ? '启用' : '禁用'
  ElMessage.success(`状态已${row.status}`)
}
</script>

<style scoped>
.bio-category {}
.card-header { display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 16px; font-weight: 600; }
.toolbar { margin-bottom: 8px; }
.pagination-wrap { display: flex; justify-content: flex-end; margin-top: 16px; }
</style>

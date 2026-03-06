<template>
  <div class="role-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">角色权限管理</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>新增角色
          </el-button>
        </div>
      </template>

      <el-row :gutter="16">
        <el-col :xs="24" :md="10">
          <el-table :data="roles" stripe border @row-click="selectRole" highlight-current-row>
            <el-table-column prop="name" label="角色名称" />
            <el-table-column prop="code" label="角色编码" />
            <el-table-column prop="userCount" label="用户数" width="80" align="center" />
            <el-table-column label="操作" width="100" align="center">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click.stop="editRole(row)">编辑</el-button>
                <el-button type="danger" link size="small" @click.stop="deleteRole(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>

        <el-col :xs="24" :md="14">
          <el-card shadow="hover" v-if="selectedRole">
            <template #header>
              <span>「{{ selectedRole.name }}」权限配置</span>
            </template>
            <p style="color:#666;margin-bottom:12px">{{ selectedRole.description }}</p>
            <el-checkbox-group v-model="selectedRole.permissions">
              <el-row :gutter="12">
                <el-col :span="12" v-for="perm in allPermissions" :key="perm.value" style="margin-bottom:12px">
                  <el-checkbox :value="perm.value" :label="perm.label">{{ perm.label }}</el-checkbox>
                </el-col>
              </el-row>
            </el-checkbox-group>
            <div style="margin-top:16px">
              <el-button type="primary" @click="savePermissions">保存权限</el-button>
            </div>
          </el-card>
          <el-empty v-else description="请点击左侧角色查看权限" />
        </el-col>
      </el-row>
    </el-card>

    <el-dialog v-model="showAddDialog" title="新增角色" width="400px">
      <el-form :model="addForm" label-width="90px">
        <el-form-item label="角色名称"><el-input v-model="addForm.name" /></el-form-item>
        <el-form-item label="角色编码"><el-input v-model="addForm.code" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="addForm.description" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { roles as mockRoles } from '@/mock/system.js'

const roles = ref(mockRoles.map(r => ({ ...r, permissions: [...r.permissions] })))
const selectedRole = ref(null)
const showAddDialog = ref(false)
const addForm = ref({ name: '', code: '', description: '' })

const allPermissions = [
  { value: 'dashboard', label: '首页/仪表盘' },
  { value: 'pond', label: '鱼塘管理' },
  { value: 'aquaculture', label: '养殖管理' },
  { value: 'water', label: '水质监测' },
  { value: 'system', label: '系统设置' }
]

const selectRole = (row) => { selectedRole.value = row }
const editRole = (row) => ElMessage.info(`编辑角色：${row.name}（功能演示）`)
const deleteRole = (row) => {
  ElMessageBox.confirm(`确定删除角色「${row.name}」吗？`, '提示', { type: 'warning' }).then(() => {
    const idx = roles.value.findIndex(r => r.id === row.id)
    if (idx !== -1) roles.value.splice(idx, 1)
    if (selectedRole.value?.id === row.id) selectedRole.value = null
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const savePermissions = () => ElMessage.success('权限配置已保存')

const handleAdd = () => {
  roles.value.push({ id: Date.now(), ...addForm.value, userCount: 0, permissions: [], createTime: new Date().toISOString().slice(0, 10) })
  showAddDialog.value = false
  ElMessage.success('角色创建成功')
  addForm.value = { name: '', code: '', description: '' }
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
</style>

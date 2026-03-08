<template>
  <div class="user-manage">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span class="title">用户管理</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>新增用户
          </el-button>
        </div>
      </template>

      <el-table :data="users" stripe border style="width:100%">
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="username" label="用户名" min-width="110" />
        <el-table-column prop="name" label="姓名" width="90" />
        <el-table-column prop="role" label="角色" width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="phone" label="手机号" width="130" />
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '正常' ? 'success' : 'danger'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastLogin" label="最后登录" min-width="160" />
        <el-table-column label="操作" width="160" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="editUser(row)">编辑</el-button>
            <el-button
              :type="row.status === '正常' ? 'warning' : 'success'"
              link size="small"
              @click="toggleStatus(row)"
            >{{ row.status === '正常' ? '禁用' : '启用' }}</el-button>
            <el-button type="danger" link size="small" @click="deleteUser(row)" :disabled="row.username === 'admin'">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showAddDialog" title="新增用户" width="480px">
      <el-form :model="addForm" label-width="90px" ref="addFormRef">
        <el-form-item label="用户名" :rules="[{required:true,message:'必填'}]" prop="username">
          <el-input v-model="addForm.username" />
        </el-form-item>
        <el-form-item label="姓名" :rules="[{required:true,message:'必填'}]" prop="name">
          <el-input v-model="addForm.name" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="addForm.role" style="width:100%">
            <el-option label="超级管理员" value="超级管理员" />
            <el-option label="养殖员" value="养殖员" />
            <el-option label="水质监测员" value="水质监测员" />
            <el-option label="访客" value="访客" />
          </el-select>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addForm.email" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="addForm.phone" />
        </el-form-item>
        <el-form-item label="初始密码" prop="password">
          <el-input v-model="addForm.password" type="password" show-password />
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
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { users as mockUsers } from '@/mock/system.js'

const users = ref([...mockUsers])
const showAddDialog = ref(false)
const addFormRef = ref(null)
const addForm = ref({ username: '', name: '', role: '养殖员', email: '', phone: '', password: '' })

const editUser = (row) => ElMessage.info(`编辑用户：${row.name}（功能演示）`)

const toggleStatus = (row) => {
  row.status = row.status === '正常' ? '禁用' : '正常'
  ElMessage.success(`用户 ${row.name} 已${row.status === '正常' ? '启用' : '禁用'}`)
}

const deleteUser = (row) => {
  ElMessageBox.confirm(`确定删除用户「${row.name}」吗？`, '提示', { type: 'warning' }).then(() => {
    const idx = users.value.findIndex(u => u.id === row.id)
    if (idx !== -1) users.value.splice(idx, 1)
    ElMessage.success('删除成功')
  }).catch(() => {})
}

const handleAdd = async () => {
  await addFormRef.value.validate()
  users.value.push({
    id: Date.now(),
    ...addForm.value,
    status: '正常',
    createTime: new Date().toISOString().slice(0, 10),
    lastLogin: '—'
  })
  showAddDialog.value = false
  ElMessage.success('用户创建成功')
  addFormRef.value.resetFields()
}
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 16px; font-weight: 600; }
</style>

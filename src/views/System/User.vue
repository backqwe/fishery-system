<template>
  <div>
    <div class="page-title">用户管理</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>用户列表</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增用户</el-button>
        </div>
      </template>
      <el-table :data="userList" stripe>
        <el-table-column prop="id" label="编号" width="60" />
        <el-table-column prop="username" label="用户名" width="110" />
        <el-table-column prop="name" label="姓名" width="90" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色" width="120" />
        <el-table-column prop="lastLogin" label="最后登录" width="160" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === '启用' ? 'success' : 'danger'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button type="primary" link size="small">编辑</el-button>
            <el-button :type="row.status === '启用' ? 'warning' : 'success'" link size="small">
              {{ row.status === '启用' ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { userList } from '@/mock/system'
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

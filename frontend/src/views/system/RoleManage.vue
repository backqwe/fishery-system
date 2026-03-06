<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>角色权限管理</template>
      <el-table :data="roles" stripe border>
        <el-table-column prop="name" label="角色名称" width="150" />
        <el-table-column prop="code" label="角色代码" width="150" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="权限">
          <template #default="{ row }">
            <el-tag v-for="p in row.permissions" :key="p" size="small" style="margin:2px">{{ p }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="userCount" label="用户数" width="90" />
        <el-table-column prop="createTime" label="创建时间" width="120" />
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button type="primary" text size="small">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { roles } from '@/mock/system.js'
</script>

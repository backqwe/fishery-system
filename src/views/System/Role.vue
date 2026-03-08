<template>
  <div>
    <div class="page-title">角色权限</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>角色列表</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增角色</el-button>
        </div>
      </template>
      <el-table :data="roleList" stripe>
        <el-table-column prop="id" label="编号" width="60" />
        <el-table-column prop="name" label="角色名称" width="140" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="权限">
          <template #default="{ row }">
            <el-tag v-for="p in row.permissions" :key="p" size="small" style="margin-right: 4px">{{ p }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="userCount" label="用户数" width="80" />
        <el-table-column prop="createTime" label="创建时间" width="110" />
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button type="primary" link size="small">编辑权限</el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { roleList } from '@/mock/system'
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

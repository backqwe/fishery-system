<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>系统日志</span>
          <el-button><el-icon><Download /></el-icon> 导出日志</el-button>
        </div>
      </template>
      <el-form :inline="true" style="margin-bottom:16px">
        <el-form-item label="用户"><el-input v-model="filterUser" placeholder="请输入用户名" clearable style="width:150px" /></el-form-item>
        <el-form-item label="模块">
          <el-select v-model="filterModule" placeholder="全部" clearable style="width:130px">
            <el-option v-for="m in ['系统','鱼塘管理','养殖管理','水质监测','系统设置']" :key="m" :label="m" :value="m" />
          </el-select>
        </el-form-item>
        <el-form-item><el-button type="primary">查询</el-button></el-form-item>
      </el-form>
      <el-table :data="logs" stripe border>
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="user" label="用户" width="120" />
        <el-table-column prop="action" label="操作" />
        <el-table-column prop="module" label="模块" width="120" />
        <el-table-column prop="ip" label="IP地址" width="140" />
        <el-table-column prop="time" label="操作时间" width="180" />
        <el-table-column label="结果" width="90">
          <template #default="{ row }">
            <el-tag :type="row.result === '成功' ? 'success' : 'danger'" size="small">{{ row.result }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { logs } from '@/mock/system.js'
const filterUser = ref('')
const filterModule = ref('')
</script>

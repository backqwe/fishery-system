<template>
  <div>
    <div class="page-title">系统日志</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>操作日志</span>
          <el-button type="danger" plain>清空日志</el-button>
        </div>
      </template>
      <el-form :inline="true" style="margin-bottom: 16px">
        <el-form-item label="操作用户">
          <el-input v-model="searchUser" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item label="模块">
          <el-select v-model="searchModule" clearable placeholder="请选择模块">
            <el-option label="系统" value="系统" />
            <el-option label="鱼塘管理" value="鱼塘管理" />
            <el-option label="养殖管理" value="养殖管理" />
            <el-option label="水质监测" value="水质监测" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">查询</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="systemLogs" stripe>
        <el-table-column prop="id" label="编号" width="60" />
        <el-table-column prop="user" label="操作用户" width="100" />
        <el-table-column prop="action" label="操作动作" width="140" />
        <el-table-column prop="module" label="所属模块" width="110" />
        <el-table-column prop="ip" label="IP地址" width="130" />
        <el-table-column prop="time" label="操作时间" width="170" />
        <el-table-column label="结果" width="80">
          <template #default="{ row }">
            <el-tag :type="row.result === '成功' ? 'success' : 'danger'" size="small">{{ row.result }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { systemLogs } from '@/mock/system'
const searchUser = ref('')
const searchModule = ref('')
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

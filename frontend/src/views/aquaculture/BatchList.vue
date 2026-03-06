<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>养殖批次</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增批次</el-button>
        </div>
      </template>
      <el-table :data="batches" stripe border>
        <el-table-column prop="batchNo" label="批次编号" width="130" />
        <el-table-column prop="pondName" label="鱼塘" width="120" />
        <el-table-column prop="species" label="养殖品种" width="100" />
        <el-table-column prop="quantity" label="放养数量" width="100" />
        <el-table-column prop="startDate" label="开始日期" width="120" />
        <el-table-column prop="expectedEnd" label="预计结束" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === '养殖中' ? 'success' : 'info'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default>
            <el-button type="primary" text size="small">查看</el-button>
            <el-button type="warning" text size="small">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { batches } from '@/mock/aquaculture.js'
</script>

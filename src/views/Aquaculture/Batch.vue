<template>
  <div>
    <div class="page-title">养殖批次</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>批次列表</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增批次</el-button>
        </div>
      </template>
      <el-table :data="batchList" stripe>
        <el-table-column prop="batchNo" label="批次号" width="130" />
        <el-table-column prop="pondName" label="鱼塘" width="100" />
        <el-table-column prop="species" label="品种" width="80" />
        <el-table-column prop="startDate" label="开始日期" width="110" />
        <el-table-column prop="estimatedEndDate" label="预计结束" width="110" />
        <el-table-column prop="stockQuantity" label="放养数量(尾)" width="120" />
        <el-table-column prop="currentQuantity" label="当前数量(尾)" width="120" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === '养殖中' ? 'success' : 'info'" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="120">
          <template #default>
            <el-button type="primary" link size="small">详情</el-button>
            <el-button type="warning" link size="small">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { batchList } from '@/mock/aquaculture'
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

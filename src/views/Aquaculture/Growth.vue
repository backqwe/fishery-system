<template>
  <div>
    <div class="page-title">生长监测</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>生长数据记录</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 录入数据</el-button>
        </div>
      </template>
      <el-table :data="growthData" stripe>
        <el-table-column prop="date" label="记录日期" width="110" />
        <el-table-column prop="batchNo" label="批次号" width="130" />
        <el-table-column prop="pondName" label="鱼塘" width="100" />
        <el-table-column prop="species" label="品种" width="80" />
        <el-table-column prop="avgWeight" label="平均体重(g)" width="120" />
        <el-table-column prop="totalWeight" label="总重量(g)" width="120" />
        <el-table-column prop="survivalRate" label="存活率(%)" width="110" />
        <el-table-column prop="notes" label="备注" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { growthData } from '@/mock/aquaculture'
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

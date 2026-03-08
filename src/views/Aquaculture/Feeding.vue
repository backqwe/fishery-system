<template>
  <div>
    <div class="page-title">投喂记录</div>
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>投喂记录列表</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增记录</el-button>
        </div>
      </template>

      <el-form :inline="true" style="margin-bottom: 16px">
        <el-form-item label="日期">
          <el-date-picker v-model="selectedDate" type="date" placeholder="选择日期" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="feedingRecords" stripe>
        <el-table-column prop="date" label="日期" width="110" />
        <el-table-column prop="pondName" label="鱼塘" width="100" />
        <el-table-column prop="feedType" label="饲料类型" width="100" />
        <el-table-column prop="amount" label="投喂量(kg)" width="110" />
        <el-table-column prop="time" label="投喂时间" width="100" />
        <el-table-column prop="operator" label="操作员" width="90" />
        <el-table-column prop="notes" label="备注" />
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button type="warning" link size="small">编辑</el-button>
            <el-button type="danger" link size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { feedingRecords } from '@/mock/aquaculture'
const selectedDate = ref('')
</script>

<style scoped>
.page-title { font-size: 20px; font-weight: bold; margin-bottom: 20px; color: #333; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

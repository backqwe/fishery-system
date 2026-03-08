<template>
  <div class="page-container">
    <el-card shadow="hover">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>投喂记录</span>
          <el-button type="primary"><el-icon><Plus /></el-icon> 新增记录</el-button>
        </div>
      </template>
      <el-form :inline="true" style="margin-bottom:16px">
        <el-form-item label="鱼塘">
          <el-select v-model="filterPond" placeholder="全部" clearable style="width:120px">
            <el-option v-for="p in ['1号鱼塘','2号鱼塘','3号鱼塘','4号鱼塘','5号鱼塘']" :key="p" :label="p" :value="p" />
          </el-select>
        </el-form-item>
        <el-form-item><el-button type="primary">查询</el-button></el-form-item>
      </el-form>
      <el-table :data="feedRecords" stripe border>
        <el-table-column prop="pondName" label="鱼塘" width="120" />
        <el-table-column prop="feedType" label="饲料类型" width="120" />
        <el-table-column prop="amount" label="投喂量" width="100">
          <template #default="{ row }">{{ row.amount }} {{ row.unit }}</template>
        </el-table-column>
        <el-table-column prop="feedTime" label="投喂时间" width="180" />
        <el-table-column prop="operator" label="操作人" width="100" />
        <el-table-column prop="remark" label="备注" />
        <el-table-column label="操作" width="100">
          <template #default>
            <el-button type="danger" text size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { feedRecords } from '@/mock/aquaculture.js'
const filterPond = ref('')
</script>

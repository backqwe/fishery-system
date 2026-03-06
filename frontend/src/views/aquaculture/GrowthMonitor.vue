<template>
  <div class="page-container">
    <el-row :gutter="16">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header>生长监测数据</template>
          <el-table :data="growthData" stripe border>
            <el-table-column prop="pondName" label="鱼塘" width="120" />
            <el-table-column prop="species" label="品种" width="100" />
            <el-table-column prop="recordDate" label="记录日期" width="120" />
            <el-table-column prop="avgWeight" label="平均体重(g)" width="130" />
            <el-table-column prop="sampleCount" label="抽样数量" width="100" />
            <el-table-column label="日增重(g)" width="110">
              <template #default="{ row }">
                <el-tag type="success" size="small">+{{ row.growthRate }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="存活率(%)" width="110">
              <template #default="{ row }">
                <el-progress :percentage="row.survivalRate" :stroke-width="6" style="width:80px" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default>
                <el-button type="primary" text size="small">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { growthData } from '@/mock/aquaculture.js'
</script>

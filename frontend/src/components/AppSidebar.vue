<template>
  <div class="sidebar">
    <div class="logo">
      <el-icon size="28" color="#1890ff"><Compass /></el-icon>
      <span v-if="!collapsed" class="logo-text">渔业管理系统</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      background-color="#001529"
      text-color="#fff"
      active-text-color="#1890ff"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/dashboard">
        <el-icon><DataLine /></el-icon>
        <template #title>仪表盘</template>
      </el-menu-item>

      <el-sub-menu index="pond">
        <template #title>
          <el-icon><Grid /></el-icon>
          <span>鱼塘管理</span>
        </template>
        <el-menu-item index="/pond/list">鱼塘列表</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="aquaculture">
        <template #title>
          <el-icon><Crop /></el-icon>
          <span>养殖管理</span>
        </template>
        <el-menu-item index="/aquaculture/batch">养殖批次</el-menu-item>
        <el-menu-item index="/aquaculture/feed">投喂记录</el-menu-item>
        <el-menu-item index="/aquaculture/growth">生长监测</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="water">
        <template #title>
          <el-icon><Monitor /></el-icon>
          <span>水质监测</span>
        </template>
        <el-menu-item index="/water/realtime">实时数据</el-menu-item>
        <el-menu-item index="/water/alert">预警设置</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="system">
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </template>
        <el-menu-item index="/system/users">用户管理</el-menu-item>
        <el-menu-item index="/system/roles">角色权限</el-menu-item>
        <el-menu-item index="/system/logs">系统日志</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

defineProps({ collapsed: Boolean })

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar { height: 100%; background: #001529; }
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid #112240;
  padding: 0 16px;
}
.logo-text {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  white-space: nowrap;
}
.sidebar-menu { border-right: none; }
</style>

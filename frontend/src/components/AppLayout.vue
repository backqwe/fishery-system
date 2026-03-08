<template>
  <el-container class="app-layout">
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="sidebar-aside">
      <AppSidebar :collapsed="isCollapsed" />
    </el-aside>
    <el-container>
      <el-header class="app-header">
        <AppHeader @toggle-sidebar="isCollapsed = !isCollapsed" />
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'

const isCollapsed = ref(false)
</script>

<style scoped>
.app-layout {
  height: 100vh;
  overflow: hidden;
}
.sidebar-aside {
  transition: width 0.3s;
  overflow: hidden;
  background-color: #001529;
}
.app-header {
  padding: 0;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.app-main {
  background: #f0f2f5;
  overflow-y: auto;
  padding: 16px;
}
</style>

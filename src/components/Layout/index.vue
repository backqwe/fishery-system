<template>
  <div class="layout-container">
    <!-- Sidebar -->
    <div class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="logo">
        <span class="logo-icon">🐟</span>
        <span class="logo-text" v-show="!isCollapsed">渔业管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapsed"
        :collapse-transition="false"
        background-color="#001529"
        text-color="#ffffffa6"
        active-text-color="#1890ff"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><Odometer /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <el-menu-item index="/fishpond">
          <el-icon><Grid /></el-icon>
          <template #title>鱼塘管理</template>
        </el-menu-item>

        <el-sub-menu index="/aquaculture">
          <template #title>
            <el-icon><Fish /></el-icon>
            <span>养殖管理</span>
          </template>
          <el-menu-item index="/aquaculture/batch">养殖批次</el-menu-item>
          <el-menu-item index="/aquaculture/feeding">投喂记录</el-menu-item>
          <el-menu-item index="/aquaculture/growth">生长监测</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="/waterquality">
          <template #title>
            <el-icon><Cloudy /></el-icon>
            <span>水质监测</span>
          </template>
          <el-menu-item index="/waterquality/monitor">实时监测</el-menu-item>
          <el-menu-item index="/waterquality/trend">趋势分析</el-menu-item>
          <el-menu-item index="/waterquality/alert">预警设置</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="/system">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统设置</span>
          </template>
          <el-menu-item index="/system/user">用户管理</el-menu-item>
          <el-menu-item index="/system/role">角色权限</el-menu-item>
          <el-menu-item index="/system/log">系统日志</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>

    <!-- Main Content -->
    <div class="main-container">
      <!-- Header -->
      <div class="header">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="isCollapsed = !isCollapsed">
            <Fold v-if="!isCollapsed" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-badge :value="3" class="notice-badge">
            <el-icon size="20"><Bell /></el-icon>
          </el-badge>
          <el-dropdown>
            <div class="user-info">
              <el-avatar :size="32" style="background-color: #1890ff">管</el-avatar>
              <span>管理员</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人设置</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- Content -->
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isCollapsed = ref(false)

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => (route.meta?.title as string) || '')
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  background-color: #001529;
  transition: width 0.3s;
  overflow: hidden;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 64px;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  background: #002140;
  overflow: hidden;
  white-space: nowrap;
}

.logo-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.logo-text {
  color: white;
  font-size: 16px;
  font-weight: bold;
  margin-left: 10px;
  white-space: nowrap;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f0f2f5;
}

.header {
  height: 60px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  cursor: pointer;
  font-size: 20px;
  color: #666;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.notice-badge {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #333;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

:deep(.el-menu) {
  border-right: none;
}
</style>

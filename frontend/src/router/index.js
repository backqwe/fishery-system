import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '仪表盘' } },
      { path: 'pond/list', name: 'PondList', component: () => import('@/views/pond/PondList.vue'), meta: { title: '鱼塘列表' } },
      { path: 'pond/detail/:id', name: 'PondDetail', component: () => import('@/views/pond/PondDetail.vue'), meta: { title: '鱼塘详情' } },
      { path: 'aquaculture/batch', name: 'BatchList', component: () => import('@/views/aquaculture/BatchList.vue'), meta: { title: '养殖批次' } },
      { path: 'aquaculture/feed', name: 'FeedRecord', component: () => import('@/views/aquaculture/FeedRecord.vue'), meta: { title: '投喂记录' } },
      { path: 'aquaculture/growth', name: 'GrowthMonitor', component: () => import('@/views/aquaculture/GrowthMonitor.vue'), meta: { title: '生长监测' } },
      { path: 'water/realtime', name: 'RealTime', component: () => import('@/views/water/RealTime.vue'), meta: { title: '实时水质' } },
      { path: 'water/alert', name: 'AlertSettings', component: () => import('@/views/water/AlertSettings.vue'), meta: { title: '预警设置' } },
      { path: 'system/users', name: 'UserManage', component: () => import('@/views/system/UserManage.vue'), meta: { title: '用户管理' } },
      { path: 'system/roles', name: 'RoleManage', component: () => import('@/views/system/RoleManage.vue'), meta: { title: '角色权限' } },
      { path: 'system/logs', name: 'SystemLog', component: () => import('@/views/system/SystemLog.vue'), meta: { title: '系统日志' } },
    ]
  }
]

export default createRouter({ history: createWebHistory(), routes })

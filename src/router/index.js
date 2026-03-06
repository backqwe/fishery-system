import { createRouter, createWebHashHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/Dashboard.vue'),
        meta: { title: '首页', icon: 'House' }
      },
      {
        path: 'pond',
        name: 'Pond',
        redirect: '/pond/list',
        meta: { title: '鱼塘管理', icon: 'Grid' },
        children: [
          {
            path: 'list',
            name: 'PondList',
            component: () => import('@/views/pond/PondList.vue'),
            meta: { title: '鱼塘列表' }
          },
          {
            path: 'detail/:id',
            name: 'PondDetail',
            component: () => import('@/views/pond/PondDetail.vue'),
            meta: { title: '鱼塘详情' }
          },
          {
            path: 'add',
            name: 'PondAdd',
            component: () => import('@/views/pond/PondForm.vue'),
            meta: { title: '新增鱼塘' }
          }
        ]
      },
      {
        path: 'aquaculture',
        name: 'Aquaculture',
        redirect: '/aquaculture/batch',
        meta: { title: '养殖管理', icon: 'Fish' },
        children: [
          {
            path: 'batch',
            name: 'AquacultureBatch',
            component: () => import('@/views/aquaculture/BatchList.vue'),
            meta: { title: '养殖批次' }
          },
          {
            path: 'feed',
            name: 'AquacultureFeed',
            component: () => import('@/views/aquaculture/FeedRecord.vue'),
            meta: { title: '投喂记录' }
          },
          {
            path: 'growth',
            name: 'AquacultureGrowth',
            component: () => import('@/views/aquaculture/GrowthMonitor.vue'),
            meta: { title: '生长监测' }
          }
        ]
      },
      {
        path: 'water',
        name: 'Water',
        redirect: '/water/realtime',
        meta: { title: '水质监测', icon: 'Drizzling' },
        children: [
          {
            path: 'realtime',
            name: 'WaterRealtime',
            component: () => import('@/views/water-quality/Realtime.vue'),
            meta: { title: '实时数据' }
          },
          {
            path: 'trend',
            name: 'WaterTrend',
            component: () => import('@/views/water-quality/Trend.vue'),
            meta: { title: '趋势分析' }
          },
          {
            path: 'threshold',
            name: 'WaterThreshold',
            component: () => import('@/views/water-quality/Threshold.vue'),
            meta: { title: '预警阈值' }
          }
        ]
      },
      {
        path: 'system',
        name: 'System',
        redirect: '/system/user',
        meta: { title: '系统设置', icon: 'Setting' },
        children: [
          {
            path: 'user',
            name: 'SystemUser',
            component: () => import('@/views/system/UserManage.vue'),
            meta: { title: '用户管理' }
          },
          {
            path: 'role',
            name: 'SystemRole',
            component: () => import('@/views/system/RoleManage.vue'),
            meta: { title: '角色权限' }
          },
          {
            path: 'log',
            name: 'SystemLog',
            component: () => import('@/views/system/SystemLog.vue'),
            meta: { title: '系统日志' }
          }
        ]
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

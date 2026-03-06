import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout/index.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Layout,
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: '仪表盘' }
        },
        {
          path: '/fishpond',
          name: 'FishPond',
          component: () => import('@/views/FishPond/Index.vue'),
          meta: { title: '鱼塘管理' }
        },
        {
          path: '/fishpond/detail/:id',
          name: 'FishPondDetail',
          component: () => import('@/views/FishPond/Detail.vue'),
          meta: { title: '鱼塘详情' }
        },
        {
          path: '/aquaculture/batch',
          name: 'AquacultureBatch',
          component: () => import('@/views/Aquaculture/Batch.vue'),
          meta: { title: '养殖批次' }
        },
        {
          path: '/aquaculture/feeding',
          name: 'AquacultureFeeding',
          component: () => import('@/views/Aquaculture/Feeding.vue'),
          meta: { title: '投喂记录' }
        },
        {
          path: '/aquaculture/growth',
          name: 'AquacultureGrowth',
          component: () => import('@/views/Aquaculture/Growth.vue'),
          meta: { title: '生长监测' }
        },
        {
          path: '/waterquality/monitor',
          name: 'WaterQualityMonitor',
          component: () => import('@/views/WaterQuality/Monitor.vue'),
          meta: { title: '水质监测' }
        },
        {
          path: '/waterquality/trend',
          name: 'WaterQualityTrend',
          component: () => import('@/views/WaterQuality/Trend.vue'),
          meta: { title: '水质趋势' }
        },
        {
          path: '/waterquality/alert',
          name: 'WaterQualityAlert',
          component: () => import('@/views/WaterQuality/Alert.vue'),
          meta: { title: '预警设置' }
        },
        {
          path: '/system/user',
          name: 'SystemUser',
          component: () => import('@/views/System/User.vue'),
          meta: { title: '用户管理' }
        },
        {
          path: '/system/role',
          name: 'SystemRole',
          component: () => import('@/views/System/Role.vue'),
          meta: { title: '角色权限' }
        },
        {
          path: '/system/log',
          name: 'SystemLog',
          component: () => import('@/views/System/Log.vue'),
          meta: { title: '系统日志' }
        }
      ]
    }
  ]
})

export default router

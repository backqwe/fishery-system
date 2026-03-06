import { createRouter, createWebHashHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'

const routes = [
  // 登录页（独立全屏，不使用 MainLayout）
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Login.vue'),
    meta: { title: '用户登录' }
  },
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
      // ── 实时监测 ──────────────────────────────
      {
        path: 'monitor',
        name: 'Monitor',
        redirect: '/monitor/realtime',
        meta: { title: '实时监测', icon: 'Monitor' },
        children: [
          {
            path: 'realtime',
            name: 'MonitorRealtime',
            component: () => import('@/views/monitor/RealtimeMonitor.vue'),
            meta: { title: '实时监测数据' }
          }
        ]
      },
      // ── 历史监测数据 ─────────────────────────────
      {
        path: 'history',
        name: 'History',
        component: () => import('@/views/history/HistoryData.vue'),
        meta: { title: '历史监测数据', icon: 'Clock' }
      },
      // ── 水质预测 ──────────────────────────────
      {
        path: 'prediction',
        name: 'Prediction',
        component: () => import('@/views/prediction/WaterPrediction.vue'),
        meta: { title: '水质预测数据', icon: 'TrendCharts' }
      },
      // ── 系统管理 ──────────────────────────────
      {
        path: 'system',
        name: 'System',
        redirect: '/system/user',
        meta: { title: '系统管理', icon: 'Setting' },
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
            meta: { title: '角色管理' }
          },
          {
            path: 'menu',
            name: 'SystemMenu',
            component: () => import('@/views/system/MenuManage.vue'),
            meta: { title: '菜单管理' }
          },
          {
            path: 'bio-category',
            name: 'SystemBioCategory',
            component: () => import('@/views/system/BioCategory.vue'),
            meta: { title: '生物类别设置' }
          },
          {
            path: 'alarm-setting',
            name: 'SystemAlarmSetting',
            component: () => import('@/views/system/AlarmSetting.vue'),
            meta: { title: '报警值设置' }
          },
          {
            path: 'log',
            name: 'SystemLog',
            component: () => import('@/views/system/SystemLog.vue'),
            meta: { title: '系统日志' }
          }
        ]
      },
      // ── 基础信息管理 ──────────────────────────────
      {
        path: 'info',
        name: 'Info',
        redirect: '/info/farm',
        meta: { title: '基础信息管理', icon: 'Grid' },
        children: [
          {
            path: 'farm',
            name: 'InfoFarm',
            component: () => import('@/views/info/FarmManage.vue'),
            meta: { title: '养殖场管理' }
          },
          {
            path: 'workshop',
            name: 'InfoWorkshop',
            component: () => import('@/views/info/WorkshopManage.vue'),
            meta: { title: '车间管理' }
          },
          {
            path: 'pond',
            name: 'InfoPond',
            component: () => import('@/views/info/PondManage.vue'),
            meta: { title: '池塘管理' }
          },
          {
            path: 'monitor-point',
            name: 'InfoMonitorPoint',
            component: () => import('@/views/info/MonitorPointManage.vue'),
            meta: { title: '监测点管理' }
          },
          {
            path: 'equipment',
            name: 'InfoEquipment',
            component: () => import('@/views/info/EquipmentManage.vue'),
            meta: { title: '设备管理' }
          }
        ]
      },
      // ── 养殖管理（原有页面保留） ─────────────────────────
      {
        path: 'aquaculture',
        name: 'Aquaculture',
        redirect: '/aquaculture/batch',
        meta: { title: '养殖管理', icon: 'Crop' },
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
      // ── 水质监测（原有页面保留） ─────────────────────────
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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 导航守卫：未登录跳转到登录页（Mock 验证 token）
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('fishery_token')
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router

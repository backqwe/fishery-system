// 仪表盘统计数据
export const dashboardStats = {
  pondCount: 8,
  speciesCount: 6,
  todayFeed: 298,
  warningCount: 2
}

// 预警通知列表
export const recentAlerts = [
  { id: 1, time: '2024-03-06 14:30', pond: '3号鱼塘', type: '水质预警', content: '溶氧量偏低(5.2mg/L)，请及时增氧', level: 'warning' },
  { id: 2, time: '2024-03-06 13:15', pond: '8号鱼塘', type: '水质预警', content: '氨氮超标(0.42mg/L)，请检查并处理', level: 'error' },
  { id: 3, time: '2024-03-06 10:00', pond: '3号鱼塘', type: '水质预警', content: 'pH值偏低(6.8)，建议施石灰调节', level: 'warning' },
  { id: 4, time: '2024-03-05 16:45', pond: '5号鱼塘', type: '设备告警', content: '增氧机运行异常，请检查', level: 'error' },
  { id: 5, time: '2024-03-05 09:30', pond: '全部鱼塘', type: '天气预警', content: '今日气温骤降，注意保暖防护', level: 'info' }
]

// 产量统计（月度）
export const yieldData = {
  months: ['2023-09', '2023-10', '2023-11', '2023-12', '2024-01', '2024-02', '2024-03'],
  yield: [12500, 15800, 18200, 22000, 8500, 6800, 4200]
}

// 养殖品种分布
export const speciesDistribution = [
  { name: '草鱼', value: 35 },
  { name: '鲤鱼', value: 25 },
  { name: '鲫鱼', value: 18 },
  { name: '鲈鱼', value: 12 },
  { name: '鲢鱼', value: 8 },
  { name: '其他', value: 2 }
]

// 最近投喂趋势（7天）
export const feedTrend = {
  dates: ['03-01', '03-02', '03-03', '03-04', '03-05', '03-06'],
  amounts: [265, 278, 290, 285, 295, 298]
}

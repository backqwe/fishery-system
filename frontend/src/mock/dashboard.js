export const stats = {
  pondCount: 24,
  speciesCount: 8,
  todayFeed: 1250,
  alertCount: 3
}

export const productionTrend = {
  months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
  data: [820, 932, 901, 934, 1290, 1330, 1320, 1500, 1480, 1650, 1700, 1800]
}

export const speciesDistribution = [
  { name: '草鱼', value: 35 },
  { name: '鲤鱼', value: 25 },
  { name: '鲫鱼', value: 20 },
  { name: '鲢鱼', value: 12 },
  { name: '其他', value: 8 }
]

export const recentAlerts = [
  { id: 1, pond: '3号鱼塘', type: '溶氧量低', value: '4.2 mg/L', time: '2024-01-15 14:30', level: 'warning' },
  { id: 2, pond: '7号鱼塘', type: 'pH值异常', value: '9.2', time: '2024-01-15 13:15', level: 'danger' },
  { id: 3, pond: '12号鱼塘', type: '水温偏高', value: '32°C', time: '2024-01-15 11:00', level: 'warning' },
  { id: 4, pond: '5号鱼塘', type: '氨氮超标', value: '0.8 mg/L', time: '2024-01-15 09:45', level: 'danger' },
  { id: 5, pond: '9号鱼塘', type: '水位下降', value: '1.2 m', time: '2024-01-14 16:20', level: 'info' }
]

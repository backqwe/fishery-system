export const statsData = [
  { title: '鱼塘总数', value: 24, unit: '个', icon: 'Fish', color: '#409EFF', trend: '+2' },
  { title: '养殖品种', value: 12, unit: '种', icon: 'Collection', color: '#67C23A', trend: '+1' },
  { title: '今日投喂量', value: 1280, unit: 'kg', icon: 'Food', color: '#E6A23C', trend: '-50' },
  { title: '预警数量', value: 3, unit: '条', icon: 'Warning', color: '#F56C6C', trend: '+1' }
]

export const productionData = {
  months: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
  series: [
    { name: '草鱼', data: [820, 932, 901, 934, 1290, 1330, 1320, 1450, 1380, 1280, 1100, 980] },
    { name: '鲢鱼', data: [620, 732, 701, 734, 1090, 1130, 1120, 1250, 1180, 1080, 900, 780] },
    { name: '鲤鱼', data: [420, 532, 501, 534, 890, 930, 920, 1050, 980, 880, 700, 580] }
  ]
}

export const pondStatusData = [
  { name: '正常', value: 18 },
  { name: '预警', value: 3 },
  { name: '维护', value: 2 },
  { name: '空置', value: 1 }
]

export const recentAlerts = [
  { id: 1, pond: '1号鱼塘', type: '水温异常', message: '水温超过28°C，当前29.5°C', time: '10分钟前', level: 'warning' },
  { id: 2, pond: '5号鱼塘', type: '溶氧量低', message: '溶氧量低于5mg/L，当前4.2mg/L', time: '25分钟前', level: 'danger' },
  { id: 3, pond: '8号鱼塘', type: 'pH值异常', message: 'pH值超过9.0，当前9.2', time: '1小时前', level: 'warning' }
]

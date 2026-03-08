export const realtimeData = [
  { id: 1, pondName: '1号鱼塘', temperature: 24.5, ph: 7.2, oxygen: 7.8, ammonia: 0.15, turbidity: 22, updateTime: '2024-01-15 14:30', status: '正常' },
  { id: 2, pondName: '2号鱼塘', temperature: 23.8, ph: 7.4, oxygen: 8.1, ammonia: 0.12, turbidity: 18, updateTime: '2024-01-15 14:30', status: '正常' },
  { id: 3, pondName: '3号鱼塘', temperature: 25.2, ph: 7.0, oxygen: 4.2, ammonia: 0.18, turbidity: 30, updateTime: '2024-01-15 14:30', status: '预警' },
  { id: 4, pondName: '4号鱼塘', temperature: 24.0, ph: 7.3, oxygen: 7.5, ammonia: 0.20, turbidity: 25, updateTime: '2024-01-15 14:30', status: '正常' },
  { id: 5, pondName: '5号鱼塘', temperature: 26.1, ph: 6.8, oxygen: 6.9, ammonia: 0.82, turbidity: 28, updateTime: '2024-01-15 14:30', status: '预警' },
  { id: 6, pondName: '7号鱼塘', temperature: 24.8, ph: 9.2, oxygen: 7.2, ammonia: 0.25, turbidity: 20, updateTime: '2024-01-15 14:30', status: '异常' }
]

export const trendData = {
  times: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
  temperature: [22.5, 23.0, 23.8, 24.5, 25.2, 25.8, 25.5, 25.0, 24.8, 24.2, 23.8],
  ph: [7.1, 7.2, 7.3, 7.2, 7.4, 7.3, 7.2, 7.1, 7.2, 7.3, 7.2],
  oxygen: [7.5, 7.8, 8.0, 7.9, 7.6, 7.4, 7.8, 8.1, 7.9, 7.6, 7.5]
}

export const alertThresholds = [
  { id: 1, param: '水温', paramKey: 'temperature', unit: '°C', minValue: 15, maxValue: 30, enabled: true },
  { id: 2, param: 'pH值', paramKey: 'ph', unit: '', minValue: 6.5, maxValue: 9.0, enabled: true },
  { id: 3, param: '溶氧量', paramKey: 'oxygen', unit: 'mg/L', minValue: 5.0, maxValue: 12.0, enabled: true },
  { id: 4, param: '氨氮', paramKey: 'ammonia', unit: 'mg/L', minValue: 0, maxValue: 0.5, enabled: true },
  { id: 5, param: '浑浊度', paramKey: 'turbidity', unit: 'NTU', minValue: 0, maxValue: 50, enabled: false }
]

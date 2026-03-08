export const currentWaterQuality = [
  { pondId: 1, pondName: '1号鱼塘', temperature: 25.6, pH: 7.2, dissolvedOxygen: 7.8, ammoniaNitrogen: 0.5, turbidity: 15, updateTime: '2024-03-01 14:30:00', status: '正常' },
  { pondId: 2, pondName: '2号鱼塘', temperature: 24.8, pH: 7.5, dissolvedOxygen: 8.2, ammoniaNitrogen: 0.3, turbidity: 12, updateTime: '2024-03-01 14:30:00', status: '正常' },
  { pondId: 3, pondName: '3号鱼塘', temperature: 26.1, pH: 7.0, dissolvedOxygen: 6.5, ammoniaNitrogen: 0.8, turbidity: 20, updateTime: '2024-03-01 14:30:00', status: '正常' },
  { pondId: 4, pondName: '4号鱼塘', temperature: 23.5, pH: 7.3, dissolvedOxygen: 7.0, ammoniaNitrogen: 0.4, turbidity: 14, updateTime: '2024-03-01 14:30:00', status: '维护' },
  { pondId: 5, pondName: '5号鱼塘', temperature: 29.5, pH: 9.2, dissolvedOxygen: 4.2, ammoniaNitrogen: 1.2, turbidity: 35, updateTime: '2024-03-01 14:30:00', status: '预警' }
]

export const waterQualityTrend = {
  times: ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00'],
  temperature: [24.5, 25.0, 25.8, 26.2, 26.8, 26.5, 25.6],
  pH: [7.0, 7.1, 7.2, 7.3, 7.4, 7.3, 7.2],
  dissolvedOxygen: [8.5, 8.2, 7.8, 7.5, 7.2, 7.5, 7.8],
  ammoniaNitrogen: [0.4, 0.45, 0.5, 0.52, 0.55, 0.52, 0.5]
}

export const alertThresholds = [
  { id: 1, parameter: '水温', minValue: 15, maxValue: 28, unit: '°C', enabled: true },
  { id: 2, parameter: 'pH值', minValue: 6.5, maxValue: 8.5, unit: '', enabled: true },
  { id: 3, parameter: '溶氧量', minValue: 5, maxValue: 12, unit: 'mg/L', enabled: true },
  { id: 4, parameter: '氨氮', minValue: 0, maxValue: 1.0, unit: 'mg/L', enabled: true },
  { id: 5, parameter: '浊度', minValue: 0, maxValue: 30, unit: 'NTU', enabled: false }
]

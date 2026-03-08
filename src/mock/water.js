// 水质实时数据
export const waterQualityRealtime = [
  { pondId: 1, pondName: '1号鱼塘', temperature: 22.5, ph: 7.2, dissolvedOxygen: 8.5, ammoniaNitrogen: 0.08, turbidity: 25, updateTime: '2024-03-06 15:30:00', status: '正常' },
  { pondId: 2, pondName: '2号鱼塘', temperature: 23.1, ph: 7.5, dissolvedOxygen: 9.0, ammoniaNitrogen: 0.06, turbidity: 22, updateTime: '2024-03-06 15:30:00', status: '正常' },
  { pondId: 3, pondName: '3号鱼塘', temperature: 24.8, ph: 6.8, dissolvedOxygen: 5.2, ammoniaNitrogen: 0.35, turbidity: 45, updateTime: '2024-03-06 15:30:00', status: '预警' },
  { pondId: 4, pondName: '4号鱼塘', temperature: 21.9, ph: 7.3, dissolvedOxygen: 8.8, ammoniaNitrogen: 0.07, turbidity: 20, updateTime: '2024-03-06 15:30:00', status: '正常' },
  { pondId: 6, pondName: '6号鱼塘', temperature: 22.3, ph: 7.1, dissolvedOxygen: 8.2, ammoniaNitrogen: 0.09, turbidity: 28, updateTime: '2024-03-06 15:30:00', status: '正常' },
  { pondId: 7, pondName: '7号鱼塘', temperature: 23.5, ph: 7.6, dissolvedOxygen: 9.2, ammoniaNitrogen: 0.05, turbidity: 18, updateTime: '2024-03-06 15:30:00', status: '正常' },
  { pondId: 8, pondName: '8号鱼塘', temperature: 25.2, ph: 6.5, dissolvedOxygen: 4.8, ammoniaNitrogen: 0.42, turbidity: 52, updateTime: '2024-03-06 15:30:00', status: '预警' }
]

// 水质趋势数据（最近7天）
export const waterTrendData = {
  dates: ['03-01', '03-02', '03-03', '03-04', '03-05', '03-06', '03-07'],
  temperature: [21.2, 21.8, 22.5, 23.1, 22.8, 22.5, 23.0],
  ph: [7.1, 7.2, 7.3, 7.2, 7.4, 7.2, 7.3],
  dissolvedOxygen: [8.2, 8.5, 8.8, 8.6, 8.9, 8.5, 8.7],
  ammoniaNitrogen: [0.08, 0.07, 0.09, 0.08, 0.07, 0.08, 0.06]
}

// 预警阈值设置
export const waterThresholds = [
  { parameter: 'temperature', label: '水温', unit: '°C', minValue: 15, maxValue: 30, warningMin: 18, warningMax: 28 },
  { parameter: 'ph', label: 'pH值', unit: '', minValue: 6.0, maxValue: 9.0, warningMin: 6.5, warningMax: 8.5 },
  { parameter: 'dissolvedOxygen', label: '溶氧量', unit: 'mg/L', minValue: 3, maxValue: 15, warningMin: 5, warningMax: 12 },
  { parameter: 'ammoniaNitrogen', label: '氨氮', unit: 'mg/L', minValue: 0, maxValue: 1.0, warningMin: 0, warningMax: 0.2 },
  { parameter: 'turbidity', label: '浑浊度', unit: 'NTU', minValue: 0, maxValue: 100, warningMin: 0, warningMax: 40 }
]

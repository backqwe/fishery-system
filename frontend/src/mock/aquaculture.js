export const batches = [
  { id: 1, batchNo: 'B2024001', pondName: '1号鱼塘', species: '草鱼', quantity: 3200, startDate: '2024-01-01', expectedEnd: '2024-12-31', status: '养殖中' },
  { id: 2, batchNo: 'B2024002', pondName: '2号鱼塘', species: '鲤鱼', quantity: 2800, startDate: '2024-01-15', expectedEnd: '2024-11-30', status: '养殖中' },
  { id: 3, batchNo: 'B2023008', pondName: '4号鱼塘', species: '鲫鱼', quantity: 1500, startDate: '2023-09-01', expectedEnd: '2024-03-31', status: '已完成' },
  { id: 4, batchNo: 'B2024003', pondName: '5号鱼塘', species: '鲢鱼', quantity: 5200, startDate: '2024-02-01', expectedEnd: '2025-01-31', status: '养殖中' },
  { id: 5, batchNo: 'B2023007', pondName: '7号鱼塘', species: '草鱼', quantity: 3800, startDate: '2023-08-01', expectedEnd: '2024-04-30', status: '已完成' }
]

export const feedRecords = [
  { id: 1, pondName: '1号鱼塘', feedType: '颗粒饲料', amount: 80, unit: 'kg', feedTime: '2024-01-15 07:30', operator: '张三', remark: '正常投喂' },
  { id: 2, pondName: '2号鱼塘', feedType: '膨化饲料', amount: 65, unit: 'kg', feedTime: '2024-01-15 07:45', operator: '李四', remark: '' },
  { id: 3, pondName: '3号鱼塘', feedType: '颗粒饲料', amount: 95, unit: 'kg', feedTime: '2024-01-15 08:00', operator: '张三', remark: '减少投喂量' },
  { id: 4, pondName: '4号鱼塘', feedType: '粉状饲料', amount: 40, unit: 'kg', feedTime: '2024-01-15 08:15', operator: '王五', remark: '' },
  { id: 5, pondName: '5号鱼塘', feedType: '颗粒饲料', amount: 120, unit: 'kg', feedTime: '2024-01-15 08:30', operator: '李四', remark: '正常投喂' },
  { id: 6, pondName: '1号鱼塘', feedType: '颗粒饲料', amount: 80, unit: 'kg', feedTime: '2024-01-15 17:00', operator: '张三', remark: '下午投喂' }
]

export const growthData = [
  { id: 1, pondName: '1号鱼塘', species: '草鱼', recordDate: '2024-01-15', avgWeight: 450, sampleCount: 20, growthRate: 2.3, survivalRate: 98.5 },
  { id: 2, pondName: '2号鱼塘', species: '鲤鱼', recordDate: '2024-01-15', avgWeight: 380, sampleCount: 20, growthRate: 1.8, survivalRate: 97.2 },
  { id: 3, pondName: '3号鱼塘', species: '草鱼', recordDate: '2024-01-15', avgWeight: 520, sampleCount: 20, growthRate: 2.5, survivalRate: 96.8 },
  { id: 4, pondName: '5号鱼塘', species: '鲢鱼', recordDate: '2024-01-15', avgWeight: 290, sampleCount: 20, growthRate: 1.5, survivalRate: 99.1 }
]

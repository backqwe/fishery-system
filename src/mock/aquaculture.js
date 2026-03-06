// 养殖批次数据
export const batches = [
  { id: 1, batchNo: 'PC202401001', pondId: 1, pondName: '1号鱼塘', species: '草鱼', quantity: 3200, weight: 0.05, startDate: '2024-01-15', expectedEndDate: '2024-10-15', status: '养殖中', manager: '张三' },
  { id: 2, batchNo: 'PC202401002', pondId: 2, pondName: '2号鱼塘', species: '鲤鱼', quantity: 5000, weight: 0.08, startDate: '2024-01-20', expectedEndDate: '2024-11-20', status: '养殖中', manager: '李四' },
  { id: 3, batchNo: 'PC202401003', pondId: 3, pondName: '3号鱼塘', species: '鲫鱼', quantity: 2800, weight: 0.04, startDate: '2024-02-01', expectedEndDate: '2024-09-01', status: '养殖中', manager: '王五' },
  { id: 4, batchNo: 'PC202312001', pondId: 4, pondName: '4号鱼塘', species: '草鱼', quantity: 4000, weight: 0.5, startDate: '2023-12-10', expectedEndDate: '2024-08-10', status: '已出塘', manager: '张三' },
  { id: 5, batchNo: 'PC202312002', pondId: 6, pondName: '6号鱼塘', species: '鲈鱼', quantity: 3800, weight: 0.06, startDate: '2024-03-05', expectedEndDate: '2024-12-05', status: '养殖中', manager: '钱七' }
]

// 投喂记录
export const feedRecords = [
  { id: 1, date: '2024-03-06', pondName: '1号鱼塘', batchNo: 'PC202401001', feedType: '颗粒饲料', amount: 45, unit: 'kg', feedTime: '08:00', operator: '张三', remark: '' },
  { id: 2, date: '2024-03-06', pondName: '2号鱼塘', batchNo: 'PC202401002', feedType: '颗粒饲料', amount: 68, unit: 'kg', feedTime: '08:30', operator: '李四', remark: '' },
  { id: 3, date: '2024-03-06', pondName: '6号鱼塘', batchNo: 'PC202312002', feedType: '鲜活饵料', amount: 30, unit: 'kg', feedTime: '09:00', operator: '钱七', remark: '水质略差，减少投喂' },
  { id: 4, date: '2024-03-05', pondName: '1号鱼塘', batchNo: 'PC202401001', feedType: '颗粒饲料', amount: 45, unit: 'kg', feedTime: '08:00', operator: '张三', remark: '' },
  { id: 5, date: '2024-03-05', pondName: '2号鱼塘', batchNo: 'PC202401002', feedType: '颗粒饲料', amount: 70, unit: 'kg', feedTime: '08:30', operator: '李四', remark: '' },
  { id: 6, date: '2024-03-05', pondName: '3号鱼塘', batchNo: 'PC202401003', feedType: '颗粒饲料', amount: 35, unit: 'kg', feedTime: '09:00', operator: '王五', remark: '' },
  { id: 7, date: '2024-03-04', pondName: '1号鱼塘', batchNo: 'PC202401001', feedType: '颗粒饲料', amount: 42, unit: 'kg', feedTime: '08:00', operator: '张三', remark: '' },
  { id: 8, date: '2024-03-04', pondName: '4号鱼塘', batchNo: 'PC202401004', feedType: '绿藻', amount: 80, unit: 'kg', feedTime: '10:00', operator: '赵六', remark: '' }
]

// 生长监测数据
export const growthData = [
  { id: 1, batchNo: 'PC202401001', date: '2024-03-01', sampleCount: 20, avgWeight: 0.15, avgLength: 12.3, survivalRate: 98.5, note: '' },
  { id: 2, batchNo: 'PC202401001', date: '2024-02-15', sampleCount: 20, avgWeight: 0.12, avgLength: 11.1, survivalRate: 99.0, note: '' },
  { id: 3, batchNo: 'PC202401001', date: '2024-02-01', sampleCount: 20, avgWeight: 0.09, avgLength: 9.8, survivalRate: 99.5, note: '' },
  { id: 4, batchNo: 'PC202401002', date: '2024-03-01', sampleCount: 20, avgWeight: 0.22, avgLength: 14.5, survivalRate: 97.8, note: '' },
  { id: 5, batchNo: 'PC202401002', date: '2024-02-15', sampleCount: 20, avgWeight: 0.18, avgLength: 13.2, survivalRate: 98.2, note: '' }
]

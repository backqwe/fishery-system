export const batchList = [
  { id: 1, batchNo: 'BN2024001', pondId: 1, pondName: '1号鱼塘', species: '草鱼', startDate: '2024-01-10', estimatedEndDate: '2024-09-10', stockQuantity: 8500, currentQuantity: 8350, status: '养殖中' },
  { id: 2, batchNo: 'BN2024002', pondId: 2, pondName: '2号鱼塘', species: '鲢鱼', startDate: '2024-01-15', estimatedEndDate: '2024-08-15', stockQuantity: 7200, currentQuantity: 7100, status: '养殖中' },
  { id: 3, batchNo: 'BN2024003', pondId: 3, pondName: '3号鱼塘', species: '鲤鱼', startDate: '2024-02-01', estimatedEndDate: '2024-10-01', stockQuantity: 10000, currentQuantity: 9900, status: '养殖中' },
  { id: 4, batchNo: 'BN2023008', pondId: 4, pondName: '4号鱼塘', species: '草鱼', startDate: '2023-03-01', estimatedEndDate: '2023-11-01', stockQuantity: 6500, currentQuantity: 0, status: '已收获' },
  { id: 5, batchNo: 'BN2024004', pondId: 5, pondName: '5号鱼塘', species: '鲫鱼', startDate: '2024-02-20', estimatedEndDate: '2024-12-20', stockQuantity: 12000, currentQuantity: 11800, status: '养殖中' }
]

export const feedingRecords = [
  { id: 1, date: '2024-03-01', pondId: 1, pondName: '1号鱼塘', feedType: '颗粒饲料', amount: 120, time: '08:30', operator: '张师傅', notes: '正常投喂' },
  { id: 2, date: '2024-03-01', pondId: 2, pondName: '2号鱼塘', feedType: '颗粒饲料', amount: 100, time: '09:00', operator: '李师傅', notes: '正常投喂' },
  { id: 3, date: '2024-03-01', pondId: 3, pondName: '3号鱼塘', feedType: '粉料', amount: 150, time: '09:30', operator: '王师傅', notes: '减少投喂' },
  { id: 4, date: '2024-03-01', pondId: 4, pondName: '4号鱼塘', feedType: '颗粒饲料', amount: 0, time: '--', operator: '--', notes: '维护中，停止投喂' },
  { id: 5, date: '2024-03-01', pondId: 5, pondName: '5号鱼塘', feedType: '颗粒饲料', amount: 180, time: '10:00', operator: '张师傅', notes: '正常投喂' },
  { id: 6, date: '2024-02-29', pondId: 1, pondName: '1号鱼塘', feedType: '颗粒饲料', amount: 130, time: '08:30', operator: '张师傅', notes: '正常投喂' },
  { id: 7, date: '2024-02-29', pondId: 2, pondName: '2号鱼塘', feedType: '颗粒饲料', amount: 110, time: '09:00', operator: '李师傅', notes: '正常投喂' }
]

export const growthData = [
  { id: 1, date: '2024-03-01', batchNo: 'BN2024001', pondName: '1号鱼塘', species: '草鱼', avgWeight: 350, totalWeight: 2922500, survivalRate: 98.2, notes: '生长良好' },
  { id: 2, date: '2024-02-15', batchNo: 'BN2024001', pondName: '1号鱼塘', species: '草鱼', avgWeight: 320, totalWeight: 2672000, survivalRate: 98.5, notes: '生长良好' },
  { id: 3, date: '2024-02-01', batchNo: 'BN2024001', pondName: '1号鱼塘', species: '草鱼', avgWeight: 285, totalWeight: 2379750, survivalRate: 98.8, notes: '生长正常' },
  { id: 4, date: '2024-03-01', batchNo: 'BN2024002', pondName: '2号鱼塘', species: '鲢鱼', avgWeight: 280, totalWeight: 1988000, survivalRate: 98.6, notes: '生长良好' },
  { id: 5, date: '2024-03-01', batchNo: 'BN2024003', pondName: '3号鱼塘', species: '鲤鱼', avgWeight: 310, totalWeight: 3069000, survivalRate: 99.0, notes: '生长优秀' }
]

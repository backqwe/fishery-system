// 鱼塘数据
export const ponds = [
  { id: 1, name: '1号鱼塘', area: 5.2, depth: 2.5, type: '草鱼塘', status: '正常', location: '东区A-01', createTime: '2023-03-15', fishCount: 3200, manager: '张三' },
  { id: 2, name: '2号鱼塘', area: 8.0, depth: 3.0, type: '鲤鱼塘', status: '正常', location: '东区A-02', createTime: '2023-04-01', fishCount: 5000, manager: '李四' },
  { id: 3, name: '3号鱼塘', area: 4.5, depth: 2.0, type: '鲫鱼塘', status: '预警', location: '西区B-01', createTime: '2023-02-20', fishCount: 2800, manager: '王五' },
  { id: 4, name: '4号鱼塘', area: 10.0, depth: 3.5, type: '混养塘', status: '正常', location: '西区B-02', createTime: '2023-01-10', fishCount: 6500, manager: '张三' },
  { id: 5, name: '5号鱼塘', area: 6.8, depth: 2.8, type: '草鱼塘', status: '维护', location: '北区C-01', createTime: '2023-05-08', fishCount: 4100, manager: '赵六' },
  { id: 6, name: '6号鱼塘', area: 7.3, depth: 3.2, type: '鲈鱼塘', status: '正常', location: '北区C-02', createTime: '2023-06-12', fishCount: 3800, manager: '钱七' },
  { id: 7, name: '7号鱼塘', area: 9.1, depth: 2.7, type: '鲢鱼塘', status: '正常', location: '南区D-01', createTime: '2023-07-03', fishCount: 5500, manager: '孙八' },
  { id: 8, name: '8号鱼塘', area: 3.5, depth: 1.8, type: '鲫鱼塘', status: '预警', location: '南区D-02', createTime: '2023-08-20', fishCount: 2000, manager: '李四' }
]

// 鱼塘状态统计
export const pondStats = {
  total: 8,
  normal: 5,
  warning: 2,
  maintenance: 1
}

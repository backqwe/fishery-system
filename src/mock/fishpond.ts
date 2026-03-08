export const fishPondList = [
  { id: 1, name: '1号鱼塘', area: 20.5, depth: 2.5, type: '淡水', species: '草鱼', status: '正常', createTime: '2023-01-15' },
  { id: 2, name: '2号鱼塘', area: 18.0, depth: 2.2, type: '淡水', species: '鲢鱼', status: '正常', createTime: '2023-01-15' },
  { id: 3, name: '3号鱼塘', area: 25.3, depth: 3.0, type: '淡水', species: '鲤鱼', status: '正常', createTime: '2023-02-20' },
  { id: 4, name: '4号鱼塘', area: 15.8, depth: 2.0, type: '淡水', species: '草鱼', status: '维护', createTime: '2023-02-20' },
  { id: 5, name: '5号鱼塘', area: 30.0, depth: 3.5, type: '淡水', species: '鲫鱼', status: '预警', createTime: '2023-03-10' },
  { id: 6, name: '6号鱼塘', area: 22.0, depth: 2.8, type: '淡水', species: '鲤鱼', status: '正常', createTime: '2023-03-10' },
  { id: 7, name: '7号鱼塘', area: 17.5, depth: 2.3, type: '淡水', species: '草鱼', status: '正常', createTime: '2023-04-05' },
  { id: 8, name: '8号鱼塘', area: 28.0, depth: 3.2, type: '淡水', species: '鲢鱼', status: '预警', createTime: '2023-04-05' }
]

export const getPondDetail = (id: number) => {
  const pond = fishPondList.find(p => p.id === id)
  return {
    ...pond,
    waterTemp: 25.6,
    pH: 7.2,
    dissolvedOxygen: 7.8,
    ammoniaNitrogen: 0.5,
    turbidity: 15,
    stockQuantity: 8500,
    feedingPerDay: 120,
    lastFeedingTime: '2024-03-01 08:30:00',
    notes: '该鱼塘水质良好，鱼群健康状态正常。'
  }
}

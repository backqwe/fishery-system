export const ponds = [
  { id: 1, name: '1号鱼塘', area: 5.2, depth: 2.5, species: '草鱼', quantity: 3200, status: '正常', createTime: '2023-03-01' },
  { id: 2, name: '2号鱼塘', area: 4.8, depth: 2.2, species: '鲤鱼', quantity: 2800, status: '正常', createTime: '2023-03-15' },
  { id: 3, name: '3号鱼塘', area: 6.1, depth: 2.8, species: '草鱼', quantity: 4100, status: '预警', createTime: '2023-04-01' },
  { id: 4, name: '4号鱼塘', area: 3.5, depth: 2.0, species: '鲫鱼', quantity: 1500, status: '正常', createTime: '2023-04-20' },
  { id: 5, name: '5号鱼塘', area: 7.2, depth: 3.0, species: '鲢鱼', quantity: 5200, status: '预警', createTime: '2023-05-10' },
  { id: 6, name: '6号鱼塘', area: 4.0, depth: 2.3, species: '鲤鱼', quantity: 2600, status: '正常', createTime: '2023-05-25' },
  { id: 7, name: '7号鱼塘', area: 5.5, depth: 2.6, species: '草鱼', quantity: 3800, status: '异常', createTime: '2023-06-01' },
  { id: 8, name: '8号鱼塘', area: 3.8, depth: 2.1, species: '鲫鱼', quantity: 1800, status: '正常', createTime: '2023-06-15' }
]

export const pondDetail = {
  id: 1,
  name: '1号鱼塘',
  area: 5.2,
  depth: 2.5,
  location: 'A区东侧',
  species: '草鱼',
  quantity: 3200,
  weight: 12800,
  status: '正常',
  createTime: '2023-03-01',
  waterParams: {
    temperature: 24.5,
    ph: 7.2,
    oxygen: 7.8,
    ammonia: 0.2,
    turbidity: 25,
    waterLevel: 2.4
  }
}

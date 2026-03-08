export const userList = [
  { id: 1, username: 'admin', name: '管理员', email: 'admin@fishery.com', role: '超级管理员', status: '启用', lastLogin: '2024-03-01 10:30:00', createTime: '2023-01-01' },
  { id: 2, username: 'zhangsan', name: '张三', email: 'zhangsan@fishery.com', role: '养殖管理员', status: '启用', lastLogin: '2024-03-01 09:15:00', createTime: '2023-02-15' },
  { id: 3, username: 'lisi', name: '李四', email: 'lisi@fishery.com', role: '水质监测员', status: '启用', lastLogin: '2024-02-28 16:45:00', createTime: '2023-03-01' },
  { id: 4, username: 'wangwu', name: '王五', email: 'wangwu@fishery.com', role: '普通用户', status: '禁用', lastLogin: '2024-01-15 11:20:00', createTime: '2023-04-10' }
]

export const roleList = [
  { id: 1, name: '超级管理员', description: '拥有所有权限', permissions: ['全部'], userCount: 1, createTime: '2023-01-01' },
  { id: 2, name: '养殖管理员', description: '管理鱼塘和养殖相关功能', permissions: ['鱼塘管理', '养殖管理', '水质监测'], userCount: 3, createTime: '2023-01-01' },
  { id: 3, name: '水质监测员', description: '负责水质监测和预警', permissions: ['水质监测'], userCount: 5, createTime: '2023-01-01' },
  { id: 4, name: '普通用户', description: '只读权限', permissions: ['查看'], userCount: 8, createTime: '2023-01-01' }
]

export const systemLogs = [
  { id: 1, user: 'admin', action: '登录系统', module: '系统', ip: '192.168.1.100', time: '2024-03-01 10:30:00', result: '成功' },
  { id: 2, user: 'admin', action: '新增鱼塘', module: '鱼塘管理', ip: '192.168.1.100', time: '2024-03-01 10:35:00', result: '成功' },
  { id: 3, user: 'zhangsan', action: '登录系统', module: '系统', ip: '192.168.1.101', time: '2024-03-01 09:15:00', result: '成功' },
  { id: 4, user: 'zhangsan', action: '录入投喂记录', module: '养殖管理', ip: '192.168.1.101', time: '2024-03-01 09:30:00', result: '成功' },
  { id: 5, user: 'lisi', action: '登录系统', module: '系统', ip: '192.168.1.102', time: '2024-02-28 16:45:00', result: '成功' },
  { id: 6, user: 'lisi', action: '更新水质数据', module: '水质监测', ip: '192.168.1.102', time: '2024-02-28 17:00:00', result: '成功' },
  { id: 7, user: 'wangwu', action: '登录系统', module: '系统', ip: '192.168.1.103', time: '2024-01-15 11:20:00', result: '失败' }
]

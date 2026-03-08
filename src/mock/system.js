// 用户数据
export const users = [
  { id: 1, username: 'admin', name: '管理员', role: '超级管理员', email: 'admin@fishery.com', phone: '13800138001', status: '正常', createTime: '2023-01-01', lastLogin: '2024-03-06 14:32:00' },
  { id: 2, username: 'zhangsan', name: '张三', role: '养殖员', email: 'zhangsan@fishery.com', phone: '13800138002', status: '正常', createTime: '2023-02-15', lastLogin: '2024-03-06 08:10:00' },
  { id: 3, username: 'lisi', name: '李四', role: '养殖员', email: 'lisi@fishery.com', phone: '13800138003', status: '正常', createTime: '2023-02-15', lastLogin: '2024-03-05 17:45:00' },
  { id: 4, username: 'wangwu', name: '王五', role: '水质监测员', email: 'wangwu@fishery.com', phone: '13800138004', status: '正常', createTime: '2023-03-01', lastLogin: '2024-03-06 09:20:00' },
  { id: 5, username: 'zhaoliu', name: '赵六', role: '养殖员', email: 'zhaoliu@fishery.com', phone: '13800138005', status: '禁用', createTime: '2023-04-10', lastLogin: '2024-02-20 16:00:00' }
]

// 角色数据
export const roles = [
  { id: 1, name: '超级管理员', code: 'SUPER_ADMIN', description: '拥有所有权限', permissions: ['dashboard', 'pond', 'aquaculture', 'water', 'system'], userCount: 1, createTime: '2023-01-01' },
  { id: 2, name: '养殖员', code: 'FARMER', description: '负责养殖日常管理', permissions: ['dashboard', 'pond', 'aquaculture'], userCount: 3, createTime: '2023-01-01' },
  { id: 3, name: '水质监测员', code: 'WATER_MONITOR', description: '负责水质监测与预警', permissions: ['dashboard', 'water'], userCount: 1, createTime: '2023-01-01' },
  { id: 4, name: '访客', code: 'VISITOR', description: '只读权限', permissions: ['dashboard'], userCount: 0, createTime: '2023-06-01' }
]

// 系统日志
export const systemLogs = [
  { id: 1, time: '2024-03-06 15:28:33', user: 'admin', action: '查看', module: '水质监测', detail: '查看1号鱼塘实时水质数据', ip: '192.168.1.100', result: '成功' },
  { id: 2, time: '2024-03-06 14:55:10', user: 'zhangsan', action: '新增', module: '投喂记录', detail: '添加1号鱼塘投喂记录', ip: '192.168.1.102', result: '成功' },
  { id: 3, time: '2024-03-06 14:32:45', user: 'admin', action: '登录', module: '系统', detail: '用户登录系统', ip: '192.168.1.100', result: '成功' },
  { id: 4, time: '2024-03-06 13:10:22', user: 'wangwu', action: '修改', module: '预警阈值', detail: '修改pH值预警阈值', ip: '192.168.1.104', result: '成功' },
  { id: 5, time: '2024-03-06 11:45:08', user: 'lisi', action: '查看', module: '养殖批次', detail: '查看2号鱼塘养殖批次', ip: '192.168.1.103', result: '成功' },
  { id: 6, time: '2024-03-06 10:30:55', user: 'admin', action: '新增', module: '鱼塘管理', detail: '新增8号鱼塘', ip: '192.168.1.100', result: '成功' },
  { id: 7, time: '2024-03-05 17:22:11', user: 'zhangsan', action: '修改', module: '鱼塘管理', detail: '修改1号鱼塘信息', ip: '192.168.1.102', result: '成功' },
  { id: 8, time: '2024-03-05 16:08:39', user: 'unknown', action: '登录', module: '系统', detail: '用户登录失败', ip: '192.168.1.200', result: '失败' }
]

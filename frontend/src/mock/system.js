export const users = [
  { id: 1, username: 'admin', name: '系统管理员', role: '超级管理员', email: 'admin@fishery.com', phone: '13800138000', status: '启用', createTime: '2023-01-01' },
  { id: 2, username: 'zhang_san', name: '张三', role: '养殖员', email: 'zhangsan@fishery.com', phone: '13800138001', status: '启用', createTime: '2023-03-15' },
  { id: 3, username: 'li_si', name: '李四', role: '养殖员', email: 'lisi@fishery.com', phone: '13800138002', status: '启用', createTime: '2023-03-20' },
  { id: 4, username: 'wang_wu', name: '王五', role: '技术员', email: 'wangwu@fishery.com', phone: '13800138003', status: '启用', createTime: '2023-04-01' },
  { id: 5, username: 'zhao_liu', name: '赵六', role: '管理员', email: 'zhaoliu@fishery.com', phone: '13800138004', status: '停用', createTime: '2023-04-15' }
]

export const roles = [
  { id: 1, name: '超级管理员', code: 'SUPER_ADMIN', description: '拥有所有权限', permissions: ['全部权限'], userCount: 1, createTime: '2023-01-01' },
  { id: 2, name: '管理员', code: 'ADMIN', description: '管理系统配置和用户', permissions: ['用户管理', '系统设置', '数据查看'], userCount: 1, createTime: '2023-01-01' },
  { id: 3, name: '技术员', code: 'TECHNICIAN', description: '负责技术监测工作', permissions: ['水质监测', '设备管理', '数据查看'], userCount: 2, createTime: '2023-01-01' },
  { id: 4, name: '养殖员', code: 'FARMER', description: '负责日常养殖管理', permissions: ['鱼塘管理', '养殖管理', '数据查看'], userCount: 5, createTime: '2023-01-01' }
]

export const logs = [
  { id: 1, user: 'admin', action: '登录系统', module: '系统', ip: '192.168.1.100', time: '2024-01-15 09:00:00', result: '成功' },
  { id: 2, user: 'zhang_san', action: '添加投喂记录', module: '养殖管理', ip: '192.168.1.101', time: '2024-01-15 09:15:23', result: '成功' },
  { id: 3, user: 'li_si', action: '修改鱼塘信息', module: '鱼塘管理', ip: '192.168.1.102', time: '2024-01-15 10:30:45', result: '成功' },
  { id: 4, user: 'admin', action: '修改预警阈值', module: '水质监测', ip: '192.168.1.100', time: '2024-01-15 11:00:12', result: '成功' },
  { id: 5, user: 'wang_wu', action: '导出水质数据', module: '水质监测', ip: '192.168.1.103', time: '2024-01-15 13:45:30', result: '成功' },
  { id: 6, user: 'zhao_liu', action: '登录系统', module: '系统', ip: '192.168.1.105', time: '2024-01-15 14:00:00', result: '失败' },
  { id: 7, user: 'zhang_san', action: '查看生长监测', module: '养殖管理', ip: '192.168.1.101', time: '2024-01-15 14:30:00', result: '成功' },
  { id: 8, user: 'admin', action: '新增用户', module: '系统设置', ip: '192.168.1.100', time: '2024-01-15 15:00:00', result: '成功' }
]

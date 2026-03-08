# 渔业管理系统 (Fishery Management System)

一个完整的渔业综合管理系统，包含 Vue 3 前端页面模板和 Python Flask 后端 API。

## 前端页面模板

### 功能模块

- **首页/仪表盘** - 数据统计卡片、ECharts 图表（产量统计、品种分布、投喂趋势）、预警通知
- **鱼塘管理** - 鱼塘列表（搜索/分页）、鱼塘详情（水质参数）、新增/编辑表单
- **养殖管理** - 养殖批次、投喂记录、生长监测（体重/存活率趋势图）
- **水质监测** - 实时数据（支持刷新）、趋势分析图、预警阈值设置
- **系统设置** - 用户管理、角色权限、系统日志

### 技术栈

- **框架**: Vue 3 + Composition API
- **构建工具**: Vite
- **UI 组件库**: Element Plus
- **图表库**: ECharts
- **路由**: Vue Router

### 快速开始

#### 环境要求

- Node.js 16+
- npm

#### 安装与运行

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 生产构建
npm run build
```

访问 `http://localhost:5173` 即可查看系统。

### 项目结构

```
fishery-system/
├── index.html              # HTML 入口
├── vite.config.js          # Vite 配置
├── package.json
├── public/
│   └── fish.svg            # 网站图标
└── src/
    ├── main.js             # 应用入口
    ├── App.vue             # 根组件
    ├── router/
    │   └── index.js        # 路由配置
    ├── layouts/
    │   └── MainLayout.vue  # 主布局（侧边栏 + Header）
    ├── mock/               # Mock 数据（可替换为真实 API）
    │   ├── dashboard.js    # 仪表盘数据
    │   ├── pond.js         # 鱼塘数据
    │   ├── aquaculture.js  # 养殖数据
    │   ├── water.js        # 水质数据
    │   └── system.js       # 系统数据
    ├── styles/
    │   └── global.css      # 全局样式
    └── views/
        ├── dashboard/      # 仪表盘
        ├── pond/           # 鱼塘管理
        ├── aquaculture/    # 养殖管理
        ├── water-quality/  # 水质监测
        └── system/         # 系统设置
```

---

## 后端 API（Python Flask）

提供鱼类品种管理、养殖池塘管理、水质监测、饲料管理和产量统计等 RESTful API。

### 技术栈

- **后端框架**: Python Flask
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）
- **ORM**: Flask-SQLAlchemy
- **API规范**: RESTful API

### 快速开始

#### 环境要求

- Python 3.8+
- pip

#### 安装步骤

1. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库：
   ```bash
   python database/init_db.py
   ```

4. 启动应用：
   ```bash
   python app.py
   ```

5. 访问 API：
   ```
   http://localhost:5000
   ```

### API 文档

详细 API 文档请参见 [docs/API.md](docs/API.md)

### 部署说明

详细部署说明请参见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 许可证

MIT License
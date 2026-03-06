# 渔业管理系统 (Fishery Management System)

一个基于 Python Flask 的渔业综合管理系统，提供鱼类品种管理、养殖池塘管理、水质监测、饲料管理和产量统计等核心功能。

## 功能模块

- **鱼类品种管理** - 管理不同鱼类品种信息（名称、描述、最适水温、生长周期等）
- **养殖池塘管理** - 池塘信息登记、状态监控（面积、容量、当前状态）
- **水质监测** - 实时记录水温、pH值、溶氧量、氨氮等水质参数
- **饲料管理** - 饲料库存管理、投喂记录追踪
- **产量统计** - 捕捞记录、产量分析与统计

## 技术栈

- **后端框架**: Python Flask
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）
- **ORM**: Flask-SQLAlchemy
- **API规范**: RESTful API

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/backqwe/fishery-system.git
   cd fishery-system
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 初始化数据库：
   ```bash
   python database/init_db.py
   ```

5. 启动应用：
   ```bash
   python app.py
   ```

6. 访问 API：
   ```
   http://localhost:5000
   ```

## API 文档

详细 API 文档请参见 [docs/API.md](docs/API.md)

## 部署说明

详细部署说明请参见 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## 项目结构

```
fishery-system/
├── app.py                  # 应用入口文件
├── config.py               # 配置文件
├── requirements.txt        # 依赖列表
├── .gitignore
├── models/                 # 数据库模型
│   ├── __init__.py
│   ├── fish_species.py     # 鱼类品种模型
│   ├── pond.py             # 养殖池塘模型
│   ├── water_quality.py    # 水质监测模型
│   ├── feed.py             # 饲料管理模型
│   └── harvest.py          # 捕捞产量模型
├── routes/                 # API 路由
│   ├── __init__.py
│   ├── fish_species.py     # 鱼类品种路由
│   ├── pond.py             # 养殖池塘路由
│   ├── water_quality.py    # 水质监测路由
│   ├── feed.py             # 饲料管理路由
│   └── harvest.py          # 产量统计路由
├── database/               # 数据库相关
│   ├── __init__.py
│   └── init_db.py          # 数据库初始化脚本
├── migrations/             # 数据库迁移文件
└── docs/                   # 文档
    ├── API.md              # API 文档
    └── DEPLOYMENT.md       # 部署说明
```

## 许可证

MIT License
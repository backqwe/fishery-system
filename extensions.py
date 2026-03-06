"""
Flask 扩展实例
独立文件避免循环导入
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# 创建扩展实例（在应用工厂函数中通过 init_app 初始化）
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

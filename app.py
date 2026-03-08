"""
渔业管理系统主入口文件
"""

import os
from flask import Flask, jsonify

from config import config
from extensions import db, migrate, cors


def create_app(config_name=None):
    """
    应用工厂函数
    :param config_name: 配置名称（development/testing/production）
    :return: Flask 应用实例
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config.get('CORS_ORIGINS', '*'))

    # 注册蓝图（路由模块）
    from routes.fish_species import fish_species_bp
    from routes.pond import pond_bp
    from routes.water_quality import water_quality_bp
    from routes.feed import feed_bp
    from routes.harvest import harvest_bp

    app.register_blueprint(fish_species_bp, url_prefix='/api/fish-species')
    app.register_blueprint(pond_bp, url_prefix='/api/ponds')
    app.register_blueprint(water_quality_bp, url_prefix='/api/water-quality')
    app.register_blueprint(feed_bp, url_prefix='/api/feed')
    app.register_blueprint(harvest_bp, url_prefix='/api/harvest')

    # 根路由 - 系统信息
    @app.route('/')
    def index():
        return jsonify({
            'system': '渔业管理系统',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'fish_species': '/api/fish-species',
                'ponds': '/api/ponds',
                'water_quality': '/api/water-quality',
                'feed': '/api/feed',
                'harvest': '/api/harvest'
            }
        })

    # 健康检查接口
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})

    # 统一错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': '资源不存在', 'message': str(e)}), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'error': '请求参数错误', 'message': str(e)}), 400

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': '服务器内部错误', 'message': str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    # 首次运行时创建所有数据库表
    with app.app_context():
        db.create_all()
    # 注意：debug=True 仅用于本地开发，生产环境请使用 gunicorn 等 WSGI 服务器
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)

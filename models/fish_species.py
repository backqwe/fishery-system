"""
鱼类品种模型
管理不同鱼类品种的基本信息
"""

from datetime import datetime
from extensions import db


class FishSpecies(db.Model):
    """鱼类品种数据模型"""

    __tablename__ = 'fish_species'

    id = db.Column(db.Integer, primary_key=True, comment='品种ID')
    name = db.Column(db.String(100), nullable=False, unique=True, comment='品种名称')
    scientific_name = db.Column(db.String(200), comment='学名')
    description = db.Column(db.Text, comment='品种描述')
    optimal_temp_min = db.Column(db.Float, comment='最适水温下限（℃）')
    optimal_temp_max = db.Column(db.Float, comment='最适水温上限（℃）')
    optimal_ph_min = db.Column(db.Float, comment='最适pH下限')
    optimal_ph_max = db.Column(db.Float, comment='最适pH上限')
    growth_cycle_days = db.Column(db.Integer, comment='生长周期（天）')
    market_price = db.Column(db.Float, comment='市场参考价格（元/斤）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, comment='更新时间')

    # 关联：一个鱼类品种可以在多个池塘中养殖
    ponds = db.relationship('Pond', back_populates='fish_species', lazy='dynamic')
    # 关联：捕捞记录
    harvests = db.relationship('Harvest', back_populates='fish_species', lazy='dynamic')

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'description': self.description,
            'optimal_temp_min': self.optimal_temp_min,
            'optimal_temp_max': self.optimal_temp_max,
            'optimal_ph_min': self.optimal_ph_min,
            'optimal_ph_max': self.optimal_ph_max,
            'growth_cycle_days': self.growth_cycle_days,
            'market_price': self.market_price,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<FishSpecies {self.name}>'

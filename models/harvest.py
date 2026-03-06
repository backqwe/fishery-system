"""
捕捞产量模型
记录捕捞作业和产量统计信息
"""

from datetime import datetime
from extensions import db


class Harvest(db.Model):
    """捕捞产量数据模型"""

    __tablename__ = 'harvests'

    # 捕捞状态
    STATUS_PLANNED = 'planned'       # 计划中
    STATUS_IN_PROGRESS = 'in_progress'  # 进行中
    STATUS_COMPLETED = 'completed'   # 已完成

    VALID_STATUSES = [STATUS_PLANNED, STATUS_IN_PROGRESS, STATUS_COMPLETED]

    id = db.Column(db.Integer, primary_key=True, comment='记录ID')
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.id'), nullable=False,
                        comment='池塘ID')
    fish_species_id = db.Column(db.Integer, db.ForeignKey('fish_species.id'),
                                comment='鱼类品种ID')
    harvest_date = db.Column(db.Date, nullable=False, comment='捕捞日期')
    quantity = db.Column(db.Float, nullable=False, comment='捕捞量（斤）')
    average_weight = db.Column(db.Float, comment='平均单尾重量（克）')
    sale_price = db.Column(db.Float, comment='销售价格（元/斤）')
    total_revenue = db.Column(db.Float, comment='总收入（元）')
    buyer = db.Column(db.String(200), comment='买家/销售渠道')
    status = db.Column(db.String(20), default=STATUS_COMPLETED, comment='状态')
    operator = db.Column(db.String(100), comment='作业人员')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, comment='更新时间')

    # 关联：池塘
    pond = db.relationship('Pond', back_populates='harvests')
    # 关联：鱼类品种
    fish_species = db.relationship('FishSpecies', back_populates='harvests')

    def calculate_revenue(self):
        """自动计算总收入"""
        if self.quantity and self.sale_price:
            return round(self.quantity * self.sale_price, 2)
        return None

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'pond_id': self.pond_id,
            'pond_name': self.pond.name if self.pond else None,
            'fish_species_id': self.fish_species_id,
            'fish_species_name': self.fish_species.name if self.fish_species else None,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'quantity': self.quantity,
            'average_weight': self.average_weight,
            'sale_price': self.sale_price,
            'total_revenue': self.total_revenue,
            'buyer': self.buyer,
            'status': self.status,
            'operator': self.operator,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Harvest pond={self.pond_id} qty={self.quantity}斤>'

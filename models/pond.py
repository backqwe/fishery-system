"""
养殖池塘模型
管理养殖池塘的基本信息和状态
"""

from datetime import datetime
from extensions import db


class Pond(db.Model):
    """养殖池塘数据模型"""

    __tablename__ = 'ponds'

    # 池塘状态枚举
    STATUS_IDLE = 'idle'           # 空闲
    STATUS_ACTIVE = 'active'       # 养殖中
    STATUS_MAINTENANCE = 'maintenance'  # 维护中
    STATUS_DISABLED = 'disabled'   # 停用

    VALID_STATUSES = [STATUS_IDLE, STATUS_ACTIVE, STATUS_MAINTENANCE, STATUS_DISABLED]

    id = db.Column(db.Integer, primary_key=True, comment='池塘ID')
    name = db.Column(db.String(100), nullable=False, unique=True, comment='池塘名称/编号')
    area = db.Column(db.Float, nullable=False, comment='池塘面积（亩）')
    depth = db.Column(db.Float, comment='池塘深度（米）')
    capacity = db.Column(db.Float, comment='最大养殖量（斤）')
    location = db.Column(db.String(200), comment='位置描述')
    status = db.Column(db.String(20), default=STATUS_IDLE, comment='池塘状态')
    fish_species_id = db.Column(db.Integer, db.ForeignKey('fish_species.id'),
                                comment='当前养殖鱼类品种ID')
    current_stock = db.Column(db.Float, default=0, comment='当前存栏量（斤）')
    stocking_date = db.Column(db.Date, comment='投苗日期')
    expected_harvest_date = db.Column(db.Date, comment='预计捕捞日期')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, comment='更新时间')

    # 关联：鱼类品种
    fish_species = db.relationship('FishSpecies', back_populates='ponds')
    # 关联：水质监测记录
    water_quality_records = db.relationship('WaterQuality', back_populates='pond',
                                            lazy='dynamic')
    # 关联：投喂记录
    feed_records = db.relationship('FeedRecord', back_populates='pond', lazy='dynamic')
    # 关联：捕捞记录
    harvests = db.relationship('Harvest', back_populates='pond', lazy='dynamic')

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'depth': self.depth,
            'capacity': self.capacity,
            'location': self.location,
            'status': self.status,
            'fish_species_id': self.fish_species_id,
            'fish_species_name': self.fish_species.name if self.fish_species else None,
            'current_stock': self.current_stock,
            'stocking_date': self.stocking_date.isoformat() if self.stocking_date else None,
            'expected_harvest_date': self.expected_harvest_date.isoformat()
                                     if self.expected_harvest_date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Pond {self.name}>'

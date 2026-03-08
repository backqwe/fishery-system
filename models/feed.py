"""
饲料管理模型
包含饲料库存和投喂记录两个模型
"""

from datetime import datetime
from extensions import db


class FeedStock(db.Model):
    """饲料库存数据模型"""

    __tablename__ = 'feed_stocks'

    id = db.Column(db.Integer, primary_key=True, comment='饲料ID')
    name = db.Column(db.String(100), nullable=False, comment='饲料名称')
    brand = db.Column(db.String(100), comment='品牌')
    feed_type = db.Column(db.String(50), comment='饲料类型（颗粒料/粉料/鲜饵等）')
    protein_content = db.Column(db.Float, comment='蛋白质含量（%）')
    unit_price = db.Column(db.Float, comment='单价（元/kg）')
    stock_quantity = db.Column(db.Float, default=0, comment='库存数量（kg）')
    min_stock_alert = db.Column(db.Float, default=100, comment='最低库存预警（kg）')
    supplier = db.Column(db.String(200), comment='供应商')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, comment='更新时间')

    # 关联：投喂记录
    feed_records = db.relationship('FeedRecord', back_populates='feed_stock', lazy='dynamic')

    @property
    def is_low_stock(self):
        """是否库存预警"""
        return self.stock_quantity <= self.min_stock_alert

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'feed_type': self.feed_type,
            'protein_content': self.protein_content,
            'unit_price': self.unit_price,
            'stock_quantity': self.stock_quantity,
            'min_stock_alert': self.min_stock_alert,
            'is_low_stock': self.is_low_stock,
            'supplier': self.supplier,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<FeedStock {self.name}>'


class FeedRecord(db.Model):
    """投喂记录数据模型"""

    __tablename__ = 'feed_records'

    id = db.Column(db.Integer, primary_key=True, comment='记录ID')
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.id'), nullable=False,
                        comment='池塘ID')
    feed_stock_id = db.Column(db.Integer, db.ForeignKey('feed_stocks.id'), nullable=False,
                              comment='饲料ID')
    quantity = db.Column(db.Float, nullable=False, comment='投喂量（kg）')
    unit_price = db.Column(db.Float, comment='投喂时单价（元/kg）')
    feed_method = db.Column(db.String(50), comment='投喂方式（手动/自动投饵机）')
    fed_by = db.Column(db.String(100), comment='投喂人员')
    feed_time = db.Column(db.DateTime, default=datetime.utcnow, comment='投喂时间')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联：池塘
    pond = db.relationship('Pond', back_populates='feed_records')
    # 关联：饲料库存
    feed_stock = db.relationship('FeedStock', back_populates='feed_records')

    @property
    def total_cost(self):
        """本次投喂总费用"""
        if self.unit_price and self.quantity:
            return round(self.unit_price * self.quantity, 2)
        return None

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'pond_id': self.pond_id,
            'pond_name': self.pond.name if self.pond else None,
            'feed_stock_id': self.feed_stock_id,
            'feed_name': self.feed_stock.name if self.feed_stock else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_cost': self.total_cost,
            'feed_method': self.feed_method,
            'fed_by': self.fed_by,
            'feed_time': self.feed_time.isoformat() if self.feed_time else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<FeedRecord pond={self.pond_id} qty={self.quantity}kg>'

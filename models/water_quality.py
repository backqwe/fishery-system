"""
水质监测模型
记录池塘水质的各项参数
"""

from datetime import datetime
from extensions import db


class WaterQuality(db.Model):
    """水质监测数据模型"""

    __tablename__ = 'water_quality'

    # 水质评级
    GRADE_EXCELLENT = 'excellent'  # 优
    GRADE_GOOD = 'good'            # 良
    GRADE_FAIR = 'fair'            # 中
    GRADE_POOR = 'poor'            # 差

    id = db.Column(db.Integer, primary_key=True, comment='记录ID')
    pond_id = db.Column(db.Integer, db.ForeignKey('ponds.id'), nullable=False,
                        comment='池塘ID')
    temperature = db.Column(db.Float, comment='水温（℃）')
    ph = db.Column(db.Float, comment='pH值')
    dissolved_oxygen = db.Column(db.Float, comment='溶解氧（mg/L）')
    ammonia_nitrogen = db.Column(db.Float, comment='氨氮（mg/L）')
    nitrite = db.Column(db.Float, comment='亚硝酸盐（mg/L）')
    turbidity = db.Column(db.Float, comment='浊度（NTU）')
    salinity = db.Column(db.Float, comment='盐度（ppt）')
    grade = db.Column(db.String(20), comment='水质评级')
    notes = db.Column(db.Text, comment='备注/异常说明')
    recorded_by = db.Column(db.String(100), comment='记录人员')
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, comment='记录时间')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')

    # 关联：池塘
    pond = db.relationship('Pond', back_populates='water_quality_records')

    def calculate_grade(self):
        """根据水质参数自动评级"""
        issues = 0

        # pH 正常范围 6.5 - 8.5
        if self.ph is not None:
            if self.ph < 6.0 or self.ph > 9.0:
                issues += 2
            elif self.ph < 6.5 or self.ph > 8.5:
                issues += 1

        # 溶解氧正常范围 > 5 mg/L
        if self.dissolved_oxygen is not None:
            if self.dissolved_oxygen < 3:
                issues += 2
            elif self.dissolved_oxygen < 5:
                issues += 1

        # 氨氮正常范围 < 0.5 mg/L
        if self.ammonia_nitrogen is not None:
            if self.ammonia_nitrogen > 1.0:
                issues += 2
            elif self.ammonia_nitrogen > 0.5:
                issues += 1

        if issues == 0:
            return self.GRADE_EXCELLENT
        elif issues == 1:
            return self.GRADE_GOOD
        elif issues == 2:
            return self.GRADE_FAIR
        else:
            return self.GRADE_POOR

    def to_dict(self):
        """将模型对象转换为字典（用于 JSON 序列化）"""
        return {
            'id': self.id,
            'pond_id': self.pond_id,
            'pond_name': self.pond.name if self.pond else None,
            'temperature': self.temperature,
            'ph': self.ph,
            'dissolved_oxygen': self.dissolved_oxygen,
            'ammonia_nitrogen': self.ammonia_nitrogen,
            'nitrite': self.nitrite,
            'turbidity': self.turbidity,
            'salinity': self.salinity,
            'grade': self.grade,
            'notes': self.notes,
            'recorded_by': self.recorded_by,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<WaterQuality pond={self.pond_id} at={self.recorded_at}>'

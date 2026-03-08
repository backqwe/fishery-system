"""
水质监测 API 路由
提供水质数据的记录和查询接口
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import db
from models.water_quality import WaterQuality
from models.pond import Pond

water_quality_bp = Blueprint('water_quality', __name__)


@water_quality_bp.route('', methods=['GET'])
def get_water_quality_records():
    """
    获取水质监测记录列表
    支持按池塘ID、日期范围筛选
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pond_id = request.args.get('pond_id', type=int)
    grade = request.args.get('grade')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = WaterQuality.query
    if pond_id:
        query = query.filter_by(pond_id=pond_id)
    if grade:
        query = query.filter_by(grade=grade)
    if start_date:
        query = query.filter(WaterQuality.recorded_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(WaterQuality.recorded_at <= datetime.fromisoformat(end_date))

    pagination = query.order_by(WaterQuality.recorded_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@water_quality_bp.route('/<int:record_id>', methods=['GET'])
def get_water_quality(record_id):
    """获取单条水质监测记录"""
    record = WaterQuality.query.get_or_404(record_id)
    return jsonify(record.to_dict())


@water_quality_bp.route('', methods=['POST'])
def create_water_quality():
    """新增水质监测记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    if not data.get('pond_id'):
        return jsonify({'error': '池塘ID不能为空'}), 400

    # 验证池塘是否存在
    if not Pond.query.get(data['pond_id']):
        return jsonify({'error': f'池塘ID {data["pond_id"]} 不存在'}), 400

    record = WaterQuality(
        pond_id=data['pond_id'],
        temperature=data.get('temperature'),
        ph=data.get('ph'),
        dissolved_oxygen=data.get('dissolved_oxygen'),
        ammonia_nitrogen=data.get('ammonia_nitrogen'),
        nitrite=data.get('nitrite'),
        turbidity=data.get('turbidity'),
        salinity=data.get('salinity'),
        notes=data.get('notes'),
        recorded_by=data.get('recorded_by')
    )

    # 处理记录时间
    if data.get('recorded_at'):
        record.recorded_at = datetime.fromisoformat(data['recorded_at'])

    # 自动评级
    record.grade = data.get('grade') or record.calculate_grade()

    db.session.add(record)
    db.session.commit()

    return jsonify({'message': '水质记录创建成功', 'data': record.to_dict()}), 201


@water_quality_bp.route('/<int:record_id>', methods=['PUT'])
def update_water_quality(record_id):
    """更新水质监测记录"""
    record = WaterQuality.query.get_or_404(record_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    updatable_fields = [
        'temperature', 'ph', 'dissolved_oxygen', 'ammonia_nitrogen',
        'nitrite', 'turbidity', 'salinity', 'notes', 'recorded_by'
    ]
    for field in updatable_fields:
        if field in data:
            setattr(record, field, data[field])

    if 'recorded_at' in data:
        record.recorded_at = datetime.fromisoformat(data['recorded_at']) \
            if data['recorded_at'] else record.recorded_at

    # 重新评级
    record.grade = data.get('grade') or record.calculate_grade()

    db.session.commit()
    return jsonify({'message': '水质记录更新成功', 'data': record.to_dict()})


@water_quality_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_water_quality(record_id):
    """删除水质监测记录"""
    record = WaterQuality.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '水质记录删除成功'})


@water_quality_bp.route('/pond/<int:pond_id>/latest', methods=['GET'])
def get_latest_water_quality(pond_id):
    """获取指定池塘的最新水质记录"""
    if not Pond.query.get(pond_id):
        return jsonify({'error': f'池塘ID {pond_id} 不存在'}), 404

    record = WaterQuality.query.filter_by(pond_id=pond_id)\
        .order_by(WaterQuality.recorded_at.desc()).first()

    if not record:
        return jsonify({'message': '该池塘暂无水质记录', 'data': None})

    return jsonify(record.to_dict())


@water_quality_bp.route('/statistics', methods=['GET'])
def water_quality_statistics():
    """获取水质统计信息（各评级数量分布）"""
    pond_id = request.args.get('pond_id', type=int)
    query = WaterQuality.query
    if pond_id:
        query = query.filter_by(pond_id=pond_id)

    total = query.count()
    grade_counts = {}
    for grade in [WaterQuality.GRADE_EXCELLENT, WaterQuality.GRADE_GOOD,
                  WaterQuality.GRADE_FAIR, WaterQuality.GRADE_POOR]:
        grade_counts[grade] = query.filter_by(grade=grade).count()

    return jsonify({
        'total_records': total,
        'grade_distribution': grade_counts
    })

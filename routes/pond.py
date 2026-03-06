"""
养殖池塘管理 API 路由
提供池塘的增删改查及状态管理接口
"""

from datetime import date
from flask import Blueprint, request, jsonify
from extensions import db
from models.pond import Pond
from models.fish_species import FishSpecies

pond_bp = Blueprint('pond', __name__)


@pond_bp.route('', methods=['GET'])
def get_ponds():
    """
    获取池塘列表
    支持分页、状态筛选和关键词搜索
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    keyword = request.args.get('keyword', '')

    query = Pond.query
    if status:
        query = query.filter_by(status=status)
    if keyword:
        query = query.filter(Pond.name.ilike(f'%{keyword}%'))

    pagination = query.order_by(Pond.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@pond_bp.route('/<int:pond_id>', methods=['GET'])
def get_pond(pond_id):
    """获取单个池塘详情"""
    pond = Pond.query.get_or_404(pond_id)
    return jsonify(pond.to_dict())


@pond_bp.route('', methods=['POST'])
def create_pond():
    """新增养殖池塘"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    # 验证必填字段
    if not data.get('name'):
        return jsonify({'error': '池塘名称不能为空'}), 400
    if not data.get('area'):
        return jsonify({'error': '池塘面积不能为空'}), 400

    # 检查是否已存在同名池塘
    if Pond.query.filter_by(name=data['name']).first():
        return jsonify({'error': f'池塘 "{data["name"]}" 已存在'}), 409

    # 验证状态值
    status = data.get('status', Pond.STATUS_IDLE)
    if status not in Pond.VALID_STATUSES:
        return jsonify({'error': f'无效的状态值，可选: {Pond.VALID_STATUSES}'}), 400

    # 验证鱼类品种
    fish_species_id = data.get('fish_species_id')
    if fish_species_id and not FishSpecies.query.get(fish_species_id):
        return jsonify({'error': f'鱼类品种ID {fish_species_id} 不存在'}), 400

    pond = Pond(
        name=data['name'],
        area=data['area'],
        depth=data.get('depth'),
        capacity=data.get('capacity'),
        location=data.get('location'),
        status=status,
        fish_species_id=fish_species_id,
        current_stock=data.get('current_stock', 0),
        notes=data.get('notes')
    )

    # 解析日期字段
    if data.get('stocking_date'):
        pond.stocking_date = date.fromisoformat(data['stocking_date'])
    if data.get('expected_harvest_date'):
        pond.expected_harvest_date = date.fromisoformat(data['expected_harvest_date'])

    db.session.add(pond)
    db.session.commit()

    return jsonify({'message': '池塘创建成功', 'data': pond.to_dict()}), 201


@pond_bp.route('/<int:pond_id>', methods=['PUT'])
def update_pond(pond_id):
    """更新池塘信息"""
    pond = Pond.query.get_or_404(pond_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    # 检查名称唯一性
    if 'name' in data and data['name'] != pond.name:
        if Pond.query.filter_by(name=data['name']).first():
            return jsonify({'error': f'池塘 "{data["name"]}" 已存在'}), 409

    # 验证状态
    if 'status' in data and data['status'] not in Pond.VALID_STATUSES:
        return jsonify({'error': f'无效的状态值，可选: {Pond.VALID_STATUSES}'}), 400

    updatable_fields = [
        'name', 'area', 'depth', 'capacity', 'location', 'status',
        'fish_species_id', 'current_stock', 'notes'
    ]
    for field in updatable_fields:
        if field in data:
            setattr(pond, field, data[field])

    if 'stocking_date' in data:
        pond.stocking_date = date.fromisoformat(data['stocking_date']) \
            if data['stocking_date'] else None
    if 'expected_harvest_date' in data:
        pond.expected_harvest_date = date.fromisoformat(data['expected_harvest_date']) \
            if data['expected_harvest_date'] else None

    db.session.commit()
    return jsonify({'message': '池塘更新成功', 'data': pond.to_dict()})


@pond_bp.route('/<int:pond_id>', methods=['DELETE'])
def delete_pond(pond_id):
    """删除池塘"""
    pond = Pond.query.get_or_404(pond_id)

    if pond.status == Pond.STATUS_ACTIVE:
        return jsonify({'error': '养殖中的池塘不能删除，请先完成捕捞或更改状态'}), 409

    db.session.delete(pond)
    db.session.commit()
    return jsonify({'message': '池塘删除成功'})


@pond_bp.route('/statistics', methods=['GET'])
def pond_statistics():
    """获取池塘统计信息"""
    total = Pond.query.count()
    status_counts = {}
    for status in Pond.VALID_STATUSES:
        status_counts[status] = Pond.query.filter_by(status=status).count()

    total_area = db.session.query(db.func.sum(Pond.area)).scalar() or 0
    total_stock = db.session.query(db.func.sum(Pond.current_stock)).scalar() or 0

    return jsonify({
        'total_ponds': total,
        'status_distribution': status_counts,
        'total_area_mu': round(total_area, 2),
        'total_current_stock_jin': round(total_stock, 2)
    })

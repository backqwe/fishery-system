"""
产量统计 API 路由
提供捕捞记录和产量分析接口
"""

from datetime import date
from flask import Blueprint, request, jsonify
from extensions import db
from models.harvest import Harvest
from models.pond import Pond
from models.fish_species import FishSpecies

harvest_bp = Blueprint('harvest', __name__)


@harvest_bp.route('', methods=['GET'])
def get_harvests():
    """
    获取捕捞记录列表
    支持按池塘、鱼类品种、日期范围筛选
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pond_id = request.args.get('pond_id', type=int)
    fish_species_id = request.args.get('fish_species_id', type=int)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Harvest.query
    if pond_id:
        query = query.filter_by(pond_id=pond_id)
    if fish_species_id:
        query = query.filter_by(fish_species_id=fish_species_id)
    if status:
        query = query.filter_by(status=status)
    if start_date:
        query = query.filter(Harvest.harvest_date >= date.fromisoformat(start_date))
    if end_date:
        query = query.filter(Harvest.harvest_date <= date.fromisoformat(end_date))

    pagination = query.order_by(Harvest.harvest_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@harvest_bp.route('/<int:harvest_id>', methods=['GET'])
def get_harvest(harvest_id):
    """获取单条捕捞记录"""
    harvest = Harvest.query.get_or_404(harvest_id)
    return jsonify(harvest.to_dict())


@harvest_bp.route('', methods=['POST'])
def create_harvest():
    """新增捕捞记录"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    if not data.get('pond_id'):
        return jsonify({'error': '池塘ID不能为空'}), 400
    if not data.get('harvest_date'):
        return jsonify({'error': '捕捞日期不能为空'}), 400
    if not data.get('quantity'):
        return jsonify({'error': '捕捞量不能为空'}), 400

    # 验证池塘和鱼类品种
    pond = Pond.query.get(data['pond_id'])
    if not pond:
        return jsonify({'error': f'池塘ID {data["pond_id"]} 不存在'}), 400

    fish_species_id = data.get('fish_species_id')
    if fish_species_id and not FishSpecies.query.get(fish_species_id):
        return jsonify({'error': f'鱼类品种ID {fish_species_id} 不存在'}), 400

    # 验证状态
    status = data.get('status', Harvest.STATUS_COMPLETED)
    if status not in Harvest.VALID_STATUSES:
        return jsonify({'error': f'无效的状态值，可选: {Harvest.VALID_STATUSES}'}), 400

    quantity = float(data['quantity'])
    sale_price = data.get('sale_price')
    total_revenue = data.get('total_revenue')

    harvest = Harvest(
        pond_id=data['pond_id'],
        fish_species_id=fish_species_id or pond.fish_species_id,
        harvest_date=date.fromisoformat(data['harvest_date']),
        quantity=quantity,
        average_weight=data.get('average_weight'),
        sale_price=sale_price,
        total_revenue=total_revenue,
        buyer=data.get('buyer'),
        status=status,
        operator=data.get('operator'),
        notes=data.get('notes')
    )

    # 自动计算总收入
    if not total_revenue and sale_price:
        harvest.total_revenue = harvest.calculate_revenue()

    # 完成捕捞时更新池塘存栏量
    if status == Harvest.STATUS_COMPLETED:
        pond.current_stock = max(0, (pond.current_stock or 0) - quantity)

    db.session.add(harvest)
    db.session.commit()

    return jsonify({'message': '捕捞记录创建成功', 'data': harvest.to_dict()}), 201


@harvest_bp.route('/<int:harvest_id>', methods=['PUT'])
def update_harvest(harvest_id):
    """更新捕捞记录"""
    harvest = Harvest.query.get_or_404(harvest_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    if 'status' in data and data['status'] not in Harvest.VALID_STATUSES:
        return jsonify({'error': f'无效的状态值，可选: {Harvest.VALID_STATUSES}'}), 400

    updatable_fields = [
        'quantity', 'average_weight', 'sale_price', 'total_revenue',
        'buyer', 'status', 'operator', 'notes'
    ]
    for field in updatable_fields:
        if field in data:
            setattr(harvest, field, data[field])

    if 'harvest_date' in data:
        harvest.harvest_date = date.fromisoformat(data['harvest_date']) \
            if data['harvest_date'] else harvest.harvest_date

    # 重新计算总收入
    if not harvest.total_revenue and harvest.sale_price:
        harvest.total_revenue = harvest.calculate_revenue()

    db.session.commit()
    return jsonify({'message': '捕捞记录更新成功', 'data': harvest.to_dict()})


@harvest_bp.route('/<int:harvest_id>', methods=['DELETE'])
def delete_harvest(harvest_id):
    """删除捕捞记录"""
    harvest = Harvest.query.get_or_404(harvest_id)
    db.session.delete(harvest)
    db.session.commit()
    return jsonify({'message': '捕捞记录删除成功'})


@harvest_bp.route('/statistics', methods=['GET'])
def harvest_statistics():
    """
    获取产量统计数据
    支持按日期范围统计总产量和总收入
    """
    pond_id = request.args.get('pond_id', type=int)
    fish_species_id = request.args.get('fish_species_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Harvest.query.filter_by(status=Harvest.STATUS_COMPLETED)
    if pond_id:
        query = query.filter_by(pond_id=pond_id)
    if fish_species_id:
        query = query.filter_by(fish_species_id=fish_species_id)
    if start_date:
        query = query.filter(Harvest.harvest_date >= date.fromisoformat(start_date))
    if end_date:
        query = query.filter(Harvest.harvest_date <= date.fromisoformat(end_date))

    total_quantity = db.session.query(
        db.func.sum(Harvest.quantity)
    ).filter(query.whereclause).scalar() or 0

    total_revenue = db.session.query(
        db.func.sum(Harvest.total_revenue)
    ).filter(query.whereclause).scalar() or 0

    record_count = query.count()

    return jsonify({
        'record_count': record_count,
        'total_quantity_jin': round(float(total_quantity), 2),
        'total_revenue_yuan': round(float(total_revenue), 2),
        'average_price_per_jin': round(float(total_revenue) / float(total_quantity), 2)
                                  if total_quantity > 0 else 0
    })

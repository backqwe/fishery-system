"""
鱼类品种管理 API 路由
提供鱼类品种的增删改查接口
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models.fish_species import FishSpecies

fish_species_bp = Blueprint('fish_species', __name__)


@fish_species_bp.route('', methods=['GET'])
def get_fish_species():
    """
    获取鱼类品种列表
    支持分页和关键词搜索
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '')

    query = FishSpecies.query
    if keyword:
        query = query.filter(
            FishSpecies.name.ilike(f'%{keyword}%') |
            FishSpecies.scientific_name.ilike(f'%{keyword}%')
        )

    pagination = query.order_by(FishSpecies.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@fish_species_bp.route('/<int:species_id>', methods=['GET'])
def get_fish_species_by_id(species_id):
    """获取单个鱼类品种详情"""
    species = FishSpecies.query.get_or_404(species_id)
    return jsonify(species.to_dict())


@fish_species_bp.route('', methods=['POST'])
def create_fish_species():
    """新增鱼类品种"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    # 验证必填字段
    if not data.get('name'):
        return jsonify({'error': '品种名称不能为空'}), 400

    # 检查是否已存在同名品种
    if FishSpecies.query.filter_by(name=data['name']).first():
        return jsonify({'error': f'品种 "{data["name"]}" 已存在'}), 409

    species = FishSpecies(
        name=data['name'],
        scientific_name=data.get('scientific_name'),
        description=data.get('description'),
        optimal_temp_min=data.get('optimal_temp_min'),
        optimal_temp_max=data.get('optimal_temp_max'),
        optimal_ph_min=data.get('optimal_ph_min'),
        optimal_ph_max=data.get('optimal_ph_max'),
        growth_cycle_days=data.get('growth_cycle_days'),
        market_price=data.get('market_price')
    )

    db.session.add(species)
    db.session.commit()

    return jsonify({'message': '鱼类品种创建成功', 'data': species.to_dict()}), 201


@fish_species_bp.route('/<int:species_id>', methods=['PUT'])
def update_fish_species(species_id):
    """更新鱼类品种信息"""
    species = FishSpecies.query.get_or_404(species_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    # 检查名称唯一性（排除自身）
    if 'name' in data and data['name'] != species.name:
        if FishSpecies.query.filter_by(name=data['name']).first():
            return jsonify({'error': f'品种 "{data["name"]}" 已存在'}), 409

    updatable_fields = [
        'name', 'scientific_name', 'description', 'optimal_temp_min',
        'optimal_temp_max', 'optimal_ph_min', 'optimal_ph_max',
        'growth_cycle_days', 'market_price'
    ]
    for field in updatable_fields:
        if field in data:
            setattr(species, field, data[field])

    db.session.commit()
    return jsonify({'message': '鱼类品种更新成功', 'data': species.to_dict()})


@fish_species_bp.route('/<int:species_id>', methods=['DELETE'])
def delete_fish_species(species_id):
    """删除鱼类品种"""
    species = FishSpecies.query.get_or_404(species_id)

    # 检查是否有关联的池塘
    if species.ponds.count() > 0:
        return jsonify({'error': '该品种已有关联的养殖池塘，无法删除'}), 409

    db.session.delete(species)
    db.session.commit()
    return jsonify({'message': '鱼类品种删除成功'})

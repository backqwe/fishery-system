"""
饲料管理 API 路由
提供饲料库存管理和投喂记录接口
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import db
from models.feed import FeedStock, FeedRecord
from models.pond import Pond

feed_bp = Blueprint('feed', __name__)


# ==================== 饲料库存管理 ====================

@feed_bp.route('/stocks', methods=['GET'])
def get_feed_stocks():
    """获取饲料库存列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    low_stock_only = request.args.get('low_stock_only', 'false').lower() == 'true'
    keyword = request.args.get('keyword', '')

    query = FeedStock.query
    if keyword:
        query = query.filter(FeedStock.name.ilike(f'%{keyword}%'))
    if low_stock_only:
        query = query.filter(FeedStock.stock_quantity <= FeedStock.min_stock_alert)

    pagination = query.order_by(FeedStock.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@feed_bp.route('/stocks/<int:stock_id>', methods=['GET'])
def get_feed_stock(stock_id):
    """获取单个饲料库存详情"""
    stock = FeedStock.query.get_or_404(stock_id)
    return jsonify(stock.to_dict())


@feed_bp.route('/stocks', methods=['POST'])
def create_feed_stock():
    """新增饲料库存"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    if not data.get('name'):
        return jsonify({'error': '饲料名称不能为空'}), 400

    stock = FeedStock(
        name=data['name'],
        brand=data.get('brand'),
        feed_type=data.get('feed_type'),
        protein_content=data.get('protein_content'),
        unit_price=data.get('unit_price'),
        stock_quantity=data.get('stock_quantity', 0),
        min_stock_alert=data.get('min_stock_alert', 100),
        supplier=data.get('supplier'),
        notes=data.get('notes')
    )

    db.session.add(stock)
    db.session.commit()
    return jsonify({'message': '饲料库存创建成功', 'data': stock.to_dict()}), 201


@feed_bp.route('/stocks/<int:stock_id>', methods=['PUT'])
def update_feed_stock(stock_id):
    """更新饲料库存信息"""
    stock = FeedStock.query.get_or_404(stock_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    updatable_fields = [
        'name', 'brand', 'feed_type', 'protein_content', 'unit_price',
        'stock_quantity', 'min_stock_alert', 'supplier', 'notes'
    ]
    for field in updatable_fields:
        if field in data:
            setattr(stock, field, data[field])

    db.session.commit()
    return jsonify({'message': '饲料库存更新成功', 'data': stock.to_dict()})


@feed_bp.route('/stocks/<int:stock_id>/restock', methods=['POST'])
def restock_feed(stock_id):
    """饲料入库（增加库存）"""
    stock = FeedStock.query.get_or_404(stock_id)
    data = request.get_json()
    if not data or not data.get('quantity'):
        return jsonify({'error': '请提供入库数量'}), 400

    quantity = float(data['quantity'])
    if quantity <= 0:
        return jsonify({'error': '入库数量必须大于0'}), 400

    stock.stock_quantity = (stock.stock_quantity or 0) + quantity
    if data.get('unit_price'):
        stock.unit_price = data['unit_price']

    db.session.commit()
    return jsonify({
        'message': f'入库成功，本次入库 {quantity} kg',
        'data': stock.to_dict()
    })


@feed_bp.route('/stocks/<int:stock_id>', methods=['DELETE'])
def delete_feed_stock(stock_id):
    """删除饲料库存"""
    stock = FeedStock.query.get_or_404(stock_id)
    if stock.feed_records.count() > 0:
        return jsonify({'error': '该饲料已有投喂记录，无法删除'}), 409

    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': '饲料库存删除成功'})


# ==================== 投喂记录管理 ====================

@feed_bp.route('/records', methods=['GET'])
def get_feed_records():
    """获取投喂记录列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    pond_id = request.args.get('pond_id', type=int)
    feed_stock_id = request.args.get('feed_stock_id', type=int)

    query = FeedRecord.query
    if pond_id:
        query = query.filter_by(pond_id=pond_id)
    if feed_stock_id:
        query = query.filter_by(feed_stock_id=feed_stock_id)

    pagination = query.order_by(FeedRecord.feed_time.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page,
        'items': [item.to_dict() for item in pagination.items]
    })


@feed_bp.route('/records/<int:record_id>', methods=['GET'])
def get_feed_record(record_id):
    """获取单条投喂记录"""
    record = FeedRecord.query.get_or_404(record_id)
    return jsonify(record.to_dict())


@feed_bp.route('/records', methods=['POST'])
def create_feed_record():
    """新增投喂记录（自动扣减饲料库存）"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '请提供有效的JSON数据'}), 400

    if not data.get('pond_id'):
        return jsonify({'error': '池塘ID不能为空'}), 400
    if not data.get('feed_stock_id'):
        return jsonify({'error': '饲料ID不能为空'}), 400
    if not data.get('quantity'):
        return jsonify({'error': '投喂量不能为空'}), 400

    # 验证池塘和饲料是否存在
    pond = Pond.query.get(data['pond_id'])
    if not pond:
        return jsonify({'error': f'池塘ID {data["pond_id"]} 不存在'}), 400

    feed_stock = FeedStock.query.get(data['feed_stock_id'])
    if not feed_stock:
        return jsonify({'error': f'饲料ID {data["feed_stock_id"]} 不存在'}), 400

    quantity = float(data['quantity'])

    # 检查库存是否充足
    if feed_stock.stock_quantity < quantity:
        return jsonify({
            'error': f'饲料库存不足，当前库存 {feed_stock.stock_quantity} kg，需要 {quantity} kg'
        }), 400

    # 创建投喂记录
    record = FeedRecord(
        pond_id=data['pond_id'],
        feed_stock_id=data['feed_stock_id'],
        quantity=quantity,
        unit_price=data.get('unit_price') or feed_stock.unit_price,
        feed_method=data.get('feed_method'),
        fed_by=data.get('fed_by'),
        notes=data.get('notes')
    )

    if data.get('feed_time'):
        record.feed_time = datetime.fromisoformat(data['feed_time'])

    # 扣减库存
    feed_stock.stock_quantity = feed_stock.stock_quantity - quantity

    db.session.add(record)
    db.session.commit()

    return jsonify({'message': '投喂记录创建成功', 'data': record.to_dict()}), 201


@feed_bp.route('/records/<int:record_id>', methods=['DELETE'])
def delete_feed_record(record_id):
    """删除投喂记录（恢复库存）"""
    record = FeedRecord.query.get_or_404(record_id)

    # 恢复饲料库存
    if record.feed_stock:
        record.feed_stock.stock_quantity = \
            (record.feed_stock.stock_quantity or 0) + record.quantity

    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '投喂记录删除成功，库存已恢复'})

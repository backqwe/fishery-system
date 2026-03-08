"""
数据库初始化脚本
创建所有数据表并插入示例数据
"""

import sys
import os

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from extensions import db
from models.fish_species import FishSpecies
from models.pond import Pond
from models.water_quality import WaterQuality
from models.feed import FeedStock, FeedRecord
from models.harvest import Harvest


def init_database():
    """初始化数据库：创建表结构并插入示例数据"""
    app = create_app('development')

    with app.app_context():
        # 删除所有现有表并重新创建（仅用于开发环境）
        print("正在删除旧表...")
        db.drop_all()

        print("正在创建数据表...")
        db.create_all()

        print("正在插入示例数据...")
        _insert_sample_data()

        print("数据库初始化完成！")


def _insert_sample_data():
    """插入示例数据"""

    # 1. 鱼类品种示例数据
    fish_list = [
        FishSpecies(
            name='草鱼',
            scientific_name='Ctenopharyngodon idella',
            description='常见淡水养殖鱼类，以水草、旱草为主食，适应性强，生长速度快。',
            optimal_temp_min=20.0,
            optimal_temp_max=30.0,
            optimal_ph_min=6.5,
            optimal_ph_max=8.5,
            growth_cycle_days=365,
            market_price=8.5
        ),
        FishSpecies(
            name='鲤鱼',
            scientific_name='Cyprinus carpio',
            description='杂食性底层鱼类，适应性强，耐低氧，全国广泛养殖。',
            optimal_temp_min=15.0,
            optimal_temp_max=28.0,
            optimal_ph_min=7.0,
            optimal_ph_max=8.5,
            growth_cycle_days=300,
            market_price=9.0
        ),
        FishSpecies(
            name='鲢鱼',
            scientific_name='Hypophthalmichthys molitrix',
            description='滤食性上层鱼类，以浮游植物为主食，有助于净化水质。',
            optimal_temp_min=18.0,
            optimal_temp_max=32.0,
            optimal_ph_min=6.5,
            optimal_ph_max=8.5,
            growth_cycle_days=270,
            market_price=7.0
        ),
        FishSpecies(
            name='罗非鱼',
            scientific_name='Oreochromis niloticus',
            description='热带鱼类，生长速度极快，耐低氧，适合高密度养殖。',
            optimal_temp_min=20.0,
            optimal_temp_max=35.0,
            optimal_ph_min=7.0,
            optimal_ph_max=9.0,
            growth_cycle_days=180,
            market_price=6.5
        ),
        FishSpecies(
            name='鲈鱼',
            scientific_name='Lateolabrax japonicus',
            description='肉食性鱼类，肉质鲜美，市场价值高，适合精品养殖。',
            optimal_temp_min=15.0,
            optimal_temp_max=28.0,
            optimal_ph_min=7.0,
            optimal_ph_max=8.5,
            growth_cycle_days=360,
            market_price=25.0
        ),
    ]

    for fish in fish_list:
        db.session.add(fish)
    db.session.flush()  # 获取自动生成的ID

    # 2. 养殖池塘示例数据
    pond_list = [
        Pond(
            name='1号池塘',
            area=5.0,
            depth=2.0,
            capacity=5000.0,
            location='东区第一排',
            status=Pond.STATUS_ACTIVE,
            fish_species_id=fish_list[0].id,
            current_stock=3000.0,
            notes='主养草鱼，配养鲢鱼'
        ),
        Pond(
            name='2号池塘',
            area=3.5,
            depth=1.8,
            capacity=3500.0,
            location='东区第二排',
            status=Pond.STATUS_ACTIVE,
            fish_species_id=fish_list[1].id,
            current_stock=2000.0,
            notes='精养鲤鱼'
        ),
        Pond(
            name='3号池塘',
            area=8.0,
            depth=2.5,
            capacity=8000.0,
            location='西区第一排',
            status=Pond.STATUS_IDLE,
            notes='休整中，下季度计划养殖罗非鱼'
        ),
        Pond(
            name='4号池塘',
            area=2.0,
            depth=1.5,
            capacity=1500.0,
            location='南区精养区',
            status=Pond.STATUS_ACTIVE,
            fish_species_id=fish_list[4].id,
            current_stock=500.0,
            notes='精养鲈鱼，高端产品'
        ),
    ]

    for pond in pond_list:
        db.session.add(pond)
    db.session.flush()

    # 3. 水质监测示例数据
    from datetime import datetime, timedelta

    water_records = []
    for i in range(7):  # 近7天的水质记录
        record_time = datetime.now() - timedelta(days=6 - i)
        water_records.append(WaterQuality(
            pond_id=pond_list[0].id,
            temperature=25.5 + i * 0.2,
            ph=7.2 + i * 0.05,
            dissolved_oxygen=6.8 - i * 0.1,
            ammonia_nitrogen=0.2 + i * 0.02,
            nitrite=0.05,
            recorded_by='张三',
            recorded_at=record_time,
            grade=WaterQuality.GRADE_EXCELLENT
        ))

    for record in water_records:
        db.session.add(record)

    # 4. 饲料库存示例数据
    feed_stocks = [
        FeedStock(
            name='草鱼专用颗粒饲料',
            brand='海大',
            feed_type='颗粒料',
            protein_content=28.0,
            unit_price=4.5,
            stock_quantity=500.0,
            min_stock_alert=100.0,
            supplier='海大集团'
        ),
        FeedStock(
            name='通用鱼料',
            brand='正大',
            feed_type='颗粒料',
            protein_content=32.0,
            unit_price=5.2,
            stock_quantity=300.0,
            min_stock_alert=80.0,
            supplier='正大集团'
        ),
        FeedStock(
            name='鲈鱼专用精料',
            brand='通威',
            feed_type='颗粒料',
            protein_content=45.0,
            unit_price=8.0,
            stock_quantity=150.0,
            min_stock_alert=50.0,
            supplier='通威股份'
        ),
    ]

    for stock in feed_stocks:
        db.session.add(stock)
    db.session.flush()

    # 5. 投喂记录示例数据
    feed_records = [
        FeedRecord(
            pond_id=pond_list[0].id,
            feed_stock_id=feed_stocks[0].id,
            quantity=25.0,
            unit_price=4.5,
            feed_method='手动投喂',
            fed_by='李四',
            feed_time=datetime.now() - timedelta(hours=6)
        ),
        FeedRecord(
            pond_id=pond_list[1].id,
            feed_stock_id=feed_stocks[1].id,
            quantity=15.0,
            unit_price=5.2,
            feed_method='自动投饵机',
            fed_by='系统',
            feed_time=datetime.now() - timedelta(hours=4)
        ),
    ]

    # 更新饲料库存（模拟已消耗）
    feed_stocks[0].stock_quantity -= 25.0
    feed_stocks[1].stock_quantity -= 15.0

    for record in feed_records:
        db.session.add(record)

    # 6. 捕捞记录示例数据
    from datetime import date

    harvests = [
        Harvest(
            pond_id=pond_list[0].id,
            fish_species_id=fish_list[0].id,
            harvest_date=date.today() - timedelta(days=30),
            quantity=1500.0,
            average_weight=750.0,
            sale_price=8.5,
            total_revenue=12750.0,
            buyer='本地市场',
            status=Harvest.STATUS_COMPLETED,
            operator='王五'
        ),
        Harvest(
            pond_id=pond_list[1].id,
            fish_species_id=fish_list[1].id,
            harvest_date=date.today() - timedelta(days=15),
            quantity=800.0,
            average_weight=900.0,
            sale_price=9.0,
            total_revenue=7200.0,
            buyer='超市批发',
            status=Harvest.STATUS_COMPLETED,
            operator='王五'
        ),
    ]

    for harvest in harvests:
        db.session.add(harvest)

    # 提交所有数据
    db.session.commit()
    print(f"  - 插入 {len(fish_list)} 种鱼类品种")
    print(f"  - 插入 {len(pond_list)} 个养殖池塘")
    print(f"  - 插入 {len(water_records)} 条水质监测记录")
    print(f"  - 插入 {len(feed_stocks)} 种饲料库存")
    print(f"  - 插入 {len(feed_records)} 条投喂记录")
    print(f"  - 插入 {len(harvests)} 条捕捞记录")


if __name__ == '__main__':
    init_database()

# 渔业管理系统 API 文档

## 基础信息

- **Base URL**: `http://localhost:5000`
- **数据格式**: JSON
- **字符编码**: UTF-8

---

## 1. 鱼类品种管理 `/api/fish-species`

### 1.1 获取鱼类品种列表

```
GET /api/fish-species
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认 1 |
| per_page | int | 否 | 每页条数，默认 20 |
| keyword | string | 否 | 搜索关键词（名称/学名） |

**响应示例**

```json
{
  "total": 5,
  "pages": 1,
  "current_page": 1,
  "per_page": 20,
  "items": [
    {
      "id": 1,
      "name": "草鱼",
      "scientific_name": "Ctenopharyngodon idella",
      "description": "常见淡水养殖鱼类...",
      "optimal_temp_min": 20.0,
      "optimal_temp_max": 30.0,
      "optimal_ph_min": 6.5,
      "optimal_ph_max": 8.5,
      "growth_cycle_days": 365,
      "market_price": 8.5,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### 1.2 获取单个鱼类品种

```
GET /api/fish-species/{id}
```

### 1.3 新增鱼类品种

```
POST /api/fish-species
```

**请求体**

```json
{
  "name": "草鱼",
  "scientific_name": "Ctenopharyngodon idella",
  "description": "常见淡水养殖鱼类",
  "optimal_temp_min": 20.0,
  "optimal_temp_max": 30.0,
  "optimal_ph_min": 6.5,
  "optimal_ph_max": 8.5,
  "growth_cycle_days": 365,
  "market_price": 8.5
}
```

### 1.4 更新鱼类品种

```
PUT /api/fish-species/{id}
```

### 1.5 删除鱼类品种

```
DELETE /api/fish-species/{id}
```

---

## 2. 养殖池塘管理 `/api/ponds`

### 2.1 获取池塘列表

```
GET /api/ponds
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码 |
| per_page | int | 否 | 每页条数 |
| status | string | 否 | 状态过滤（idle/active/maintenance/disabled） |
| keyword | string | 否 | 搜索关键词 |

### 2.2 获取单个池塘

```
GET /api/ponds/{id}
```

### 2.3 新增池塘

```
POST /api/ponds
```

**请求体**

```json
{
  "name": "1号池塘",
  "area": 5.0,
  "depth": 2.0,
  "capacity": 5000.0,
  "location": "东区第一排",
  "status": "active",
  "fish_species_id": 1,
  "current_stock": 3000.0,
  "stocking_date": "2024-01-01",
  "expected_harvest_date": "2024-12-31",
  "notes": "备注信息"
}
```

**状态说明**

| 值 | 含义 |
|----|------|
| idle | 空闲 |
| active | 养殖中 |
| maintenance | 维护中 |
| disabled | 停用 |

### 2.4 更新池塘

```
PUT /api/ponds/{id}
```

### 2.5 删除池塘

```
DELETE /api/ponds/{id}
```

### 2.6 池塘统计

```
GET /api/ponds/statistics
```

**响应示例**

```json
{
  "total_ponds": 4,
  "status_distribution": {
    "idle": 1,
    "active": 2,
    "maintenance": 0,
    "disabled": 1
  },
  "total_area_mu": 18.5,
  "total_current_stock_jin": 5500.0
}
```

---

## 3. 水质监测 `/api/water-quality`

### 3.1 获取水质记录列表

```
GET /api/water-quality
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pond_id | int | 否 | 按池塘筛选 |
| grade | string | 否 | 按评级筛选（excellent/good/fair/poor） |
| start_date | datetime | 否 | 开始时间（ISO 8601） |
| end_date | datetime | 否 | 结束时间（ISO 8601） |

### 3.2 新增水质记录

```
POST /api/water-quality
```

**请求体**

```json
{
  "pond_id": 1,
  "temperature": 25.5,
  "ph": 7.2,
  "dissolved_oxygen": 6.8,
  "ammonia_nitrogen": 0.2,
  "nitrite": 0.05,
  "turbidity": 15.0,
  "salinity": 0.5,
  "recorded_by": "张三",
  "notes": "正常"
}
```

**水质评级说明**

| 评级 | 含义 | 标准 |
|------|------|------|
| excellent | 优 | 所有指标均在正常范围内 |
| good | 良 | 1项指标轻微偏差 |
| fair | 中 | 2项指标偏差 |
| poor | 差 | 3项及以上指标偏差 |

### 3.3 获取池塘最新水质

```
GET /api/water-quality/pond/{pond_id}/latest
```

### 3.4 水质统计

```
GET /api/water-quality/statistics?pond_id={pond_id}
```

---

## 4. 饲料管理 `/api/feed`

### 4.1 饲料库存

#### 获取饲料列表

```
GET /api/feed/stocks
```

**查询参数**: `low_stock_only=true` 可只显示库存预警的饲料

#### 新增饲料

```
POST /api/feed/stocks
```

```json
{
  "name": "草鱼专用颗粒饲料",
  "brand": "海大",
  "feed_type": "颗粒料",
  "protein_content": 28.0,
  "unit_price": 4.5,
  "stock_quantity": 500.0,
  "min_stock_alert": 100.0,
  "supplier": "海大集团"
}
```

#### 饲料入库

```
POST /api/feed/stocks/{id}/restock
```

```json
{
  "quantity": 200.0,
  "unit_price": 4.5
}
```

### 4.2 投喂记录

#### 获取投喂记录

```
GET /api/feed/records?pond_id={id}
```

#### 新增投喂记录（自动扣减库存）

```
POST /api/feed/records
```

```json
{
  "pond_id": 1,
  "feed_stock_id": 1,
  "quantity": 25.0,
  "feed_method": "手动投喂",
  "fed_by": "李四"
}
```

---

## 5. 产量统计 `/api/harvest`

### 5.1 获取捕捞记录

```
GET /api/harvest
```

**查询参数**

| 参数 | 类型 | 说明 |
|------|------|------|
| pond_id | int | 按池塘筛选 |
| fish_species_id | int | 按鱼类品种筛选 |
| status | string | 按状态筛选 |
| start_date | date | 开始日期（YYYY-MM-DD） |
| end_date | date | 结束日期（YYYY-MM-DD） |

### 5.2 新增捕捞记录

```
POST /api/harvest
```

```json
{
  "pond_id": 1,
  "fish_species_id": 1,
  "harvest_date": "2024-06-01",
  "quantity": 1500.0,
  "average_weight": 750.0,
  "sale_price": 8.5,
  "buyer": "本地市场",
  "status": "completed",
  "operator": "王五"
}
```

**状态说明**: `planned`（计划中）/ `in_progress`（进行中）/ `completed`（已完成）

### 5.3 产量统计

```
GET /api/harvest/statistics?start_date=2024-01-01&end_date=2024-12-31
```

**响应示例**

```json
{
  "record_count": 12,
  "total_quantity_jin": 15000.0,
  "total_revenue_yuan": 135000.0,
  "average_price_per_jin": 9.0
}
```

---

## 错误码说明

| HTTP 状态码 | 含义 |
|------------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 409 | 冲突（如重复名称、状态不允许操作等） |
| 500 | 服务器内部错误 |

# 房产API文档

## 基础信息
- 基础URL: `/api/properties/`
- 数据库连接: `mysql://root:zhw7kqcd@test-db-mysql.ns-jj1vgrim.svc:3306/aisale`
- 字符集: utf8mb4
- 时区: Asia/Shanghai
- 测试数据库: test_aisale_new

## 数据模型

### Property (房源)
```python
class Property:
    # 表名: properties
    id: BigAutoField        # 主键
    title: CharField        # 标题
    description: TextField  # 描述
    price: IntegerField    # 总价(元)
    perprice: IntegerField # 单价(元/平方米)
    rooms: CharField       # 房间数
    areas: CharField       # 面积(平方米)
    direction: CharField   # 朝向
    zhuangXiu: CharField  # 装修
    floor: CharField      # 楼层
    Structure: CharField  # 结构
    features: CharField   # 特点
    url: CharField        # 链接
    created_at: DateTimeField  # 创建时间
    updated_at: DateTimeField  # 更新时间
    is_available: BooleanField # 是否可用
```

### PropertyImage (房源图片)
```python
class PropertyImage:
    # 表名: property_images
    id: BigAutoField     # 主键
    image_url: CharField     # 图片URL
    is_main: BooleanField # 是否主图(默认为True，因为每个房源只有一张图片)
    property: ForeignKey  # 关联房源(property_id)
```

### Favorite (收藏)
```python
class Favorite:
    # 表名: favorites
    id: AutoField       # 主键
    user: ForeignKey    # 关联用户(user_id)
    property: ForeignKey # 关联房源(property_id)
    created_at: DateTimeField # 创建时间
```

## API 端点列表

### 1. 获取房源列表
- **URL**: `/api/properties/`
- **方法**: `GET`
- **权限**: 所有用户
- **分页**: 默认每页10条
- **过滤参数**:
  - `q`: 搜索关键词
  - `min_price`: 最低价格
  - `max_price`: 最高价格
  - `rooms`: 房间数
  - `min_area`: 最小面积
  - `max_area`: 最大面积
  - `page`: 页码
  - `page_size`: 每页数量(最大100)
  - `ordering`: 排序字段(-price表示价格降序)

**请求示例**:
```javascript
axios.get('/api/properties/', {
  params: {
    q: '海景房',
    min_price: 1000000,
    max_price: 5000000,
    rooms: '3',
    page: 1,
    page_size: 10,
    ordering: '-price'
  }
})
```

**响应示例**:
```json
{
  "count": 100,
  "next": "http://api/properties/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "海景三房",
      "description": "精装修海景房",
      "price": 3000000,
      "perprice": 30000,
      "rooms": "3",
      "areas": "100",
      "direction": "南",
      "zhuangXiu": "精装",
      "floor": "高层",
      "Structure": "平层",
      "features": "海景,地铁",
      "url": "https://example.com/property/1",
      "is_available": true,
      "created_at": "2024-03-26T04:21:00Z",
      "updated_at": "2024-03-26T04:21:00Z",
      "images": [
        {
          "id": 1,
          "image_url": "https://example.com/images/1.jpg",
          "is_main": true
        }
      ]
    }
  ]
}
```

### 2. 获取房源详情
- **URL**: `/api/properties/<id>/`
- **方法**: `GET`
- **权限**: 所有用户

**请求示例**:
```javascript
axios.get('/api/properties/1/')
```

**响应示例**:
```json
{
  "id": 1,
  "title": "海景三房",
  "description": "精装修海景房",
  "price": 3000000,
  "perprice": 30000,
  "rooms": "3",
  "areas": "100",
  "direction": "南",
  "zhuangXiu": "精装",
  "floor": "高层",
  "Structure": "平层",
  "features": "海景,地铁",
  "url": "https://example.com/property/1",
  "is_available": true,
  "created_at": "2024-03-26T04:21:00Z",
  "updated_at": "2024-03-26T04:21:00Z",
  "images": [
    {
      "id": 1,
      "image_url": "https://example.com/images/1.jpg",
      "is_main": true
    }
  ]
}
```

### 3. 创建新房源
- **URL**: `/api/properties/`
- **方法**: `POST`
- **权限**: 已认证用户
- **Content-Type**: `application/json`

**请求示例**:
```javascript
axios.post('/api/properties/', {
  title: "现代化公寓",
  description: "市中心精装修公寓",
  price: 2000000,
  perprice: 20000,
  rooms: "2",
  areas: "100",
  direction: "南",
  zhuangXiu: "精装",
  floor: "中层",
  Structure: "平层",
  features: "地铁,学区",
  url: "https://example.com/property/new"
}, {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})
```

### 4. 更新房源信息
- **URL**: `/api/properties/<id>/`
- **方法**: `PUT`/`PATCH`
- **权限**: 已认证用户(仅房源所有者)

**请求示例**:
```javascript
axios.patch('/api/properties/1/', {
  price: 2100000,
  description: "更新后的描述",
  url: "https://example.com/property/1/updated"
}, {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})
```

### 5. 删除房源
- **URL**: `/api/properties/<id>/`
- **方法**: `DELETE`
- **权限**: 已认证用户(仅房源所有者)

**请求示例**:
```javascript
axios.delete('/api/properties/1/', {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})
```

### 6. 收藏/取消收藏房源
- **URL**: `/api/properties/<id>/favorite/`
- **方法**: `POST`(收藏)/`DELETE`(取消收藏)
- **权限**: 已认证用户

**请求示例**:
```javascript
// 收藏房源
axios.post('/api/properties/1/favorite/', {}, {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})

// 取消收藏
axios.delete('/api/properties/1/favorite/', {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})
```

### 7. 获取我的收藏列表
- **URL**: `/api/favorites/`
- **方法**: `GET`
- **权限**: 已认证用户

**请求示例**:
```javascript
axios.get('/api/favorites/', {
  headers: {
    'Authorization': 'Bearer your_token_here'
  }
})
```

## 错误处理
API 会返回适当的HTTP状态码：
- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未认证
- 403: 权限不足
- 404: 资源不存在
- 500: 服务器错误

## 认证
所有需要认证的接口都需要在请求头中携带JWT token：
```javascript
{
  'Authorization': 'Bearer your_token_here'
}
```

## 注意事项
1. 所有涉及金额的字段单位均为元
2. 面积单位为平方米
3. 分页默认每页10条数据，最大支持100条
4. 排序支持的字段包括：price(价格)、areas(面积)、created_at(创建时间)
5. 房源链接(url)必须是有效的URL地址


# AI 房产销售助手

一个基于 Django 和 Vue.js 的智能房产销售助手系统，提供房源管理、智能对话等功能。

## 功能特点

- 房源管理：支持房源的增删改查
- 智能对话：基于 AI 的房产咨询对话
- 图片代理：解决跨域图片加载问题
- 用户管理：支持用户注册和登录
- 收藏功能：支持房源收藏

## 技术栈

### 后端
- Django 4.2
- Django REST framework
- MySQL
- Redis (用于缓存)

### 前端
- Vue.js
- Vite
- Element Plus
- Axios

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/yourusername/ai-sales-assistant.git
cd ai-sales-assistant
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

4. 配置数据库
- 创建 MySQL 数据库
- 修改 `backend/real_estate_ai/settings.py` 中的数据库配置

5. 运行数据库迁移
```bash
python manage.py migrate
```

6. 启动后端服务
```bash
python manage.py runserver
```

7. 安装前端依赖
```bash
cd frontend
npm install
```

8. 启动前端服务
```bash
npm run dev
```

## API 文档

API 文档位于 `backend/properties/房产api.md`

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件 
# AI房产销售系统 API 文档

## 基础信息
- 基础URL: `http://localhost:8000`
- 所有请求和响应均使用JSON格式
- 需要认证的接口需要在请求头中包含会话cookie

## 用户认证相关接口

### 1. 用户注册
- 请求路径: `/api/auth/register/`
- 请求方法: POST
- 请求参数:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string",  // 密码
    "phone": "string",     // 手机号
    "email": "string"      // 邮箱(可选)
  }
  ```
- 响应示例:
  ```json
  {
    "message": "注册成功",
    "user": {
      "id": 1,
      "username": "testuser",
      "phone": "13800138000",
      "email": ""
    }
  }
  ```

### 2. 用户登录
- 请求路径: `/api/auth/login/`
- 请求方法: POST
- 请求参数:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string"   // 密码
  }
  ```
- 响应示例:
  ```json
  {
    "message": "登录成功"
  }
  ```

### 3. 用户退出
- 请求路径: `/api/auth/logout/`
- 请求方法: POST
- 需要认证: 是
- 响应示例:
  ```json
  {
    "message": "退出成功"
  }
  ```

### 4. 获取用户资料
- 请求路径: `/api/auth/profile/`
- 请求方法: GET
- 需要认证: 是
- 响应示例:
  ```json
  {
    "username": "testuser",
    "phone": "13800138000",
    "email": "",
    "is_verified": false,
    "avatar_url": null,
    "member_level": "normal",
    "house_intention": null,
    "preferred_area": null,
    "avatar": null,
    "bio": ""
  }
  ```

### 5. 更新用户资料
- 请求路径: `/api/auth/profile/`
- 请求方法: PUT/PATCH
- 需要认证: 是
- 请求参数:
  ```json
  {
    "bio": "string",      // 个人简介
    "avatar": "file"      // 头像文件
  }
  ```
- 响应示例:
  ```json
  {
    "message": "个人资料更新成功"
  }
  ```

### 6. 手机验证
- 请求路径: `/api/auth/verify-phone/`
- 请求方法: POST
- 需要认证: 是
- 请求参数:
  ```json
  {
    "code": "string"  // 验证码
  }
  ```
- 响应示例:
  ```json
  {
    "message": "手机验证成功"
  }
  ```

## 错误响应
所有接口在发生错误时会返回以下格式:
```json
{
  "error": "错误信息描述"
}
```

常见HTTP状态码:
- 200: 请求成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误 
# JWT认证API使用文档

本文档详细说明如何使用基于JWT的认证机制访问受保护的API端点。

## 认证流程概述

1. **用户登录**：发送POST请求到`/api/login`，提供用户名和密码
2. **获取JWT令牌**：登录成功后，API将返回`access_token`
3. **访问受保护资源**：在后续请求的Authorization头中包含JWT令牌
4. **令牌过期处理**：当令牌过期时，需要重新登录获取新令牌

## API端点详细说明

### 1. 用户登录

**请求**:
- 方法: POST
- URL: `/api/login`
- Content-Type: application/json
- 请求体:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**响应**:
- 成功(200 OK):
```json
{
  "message": "登录成功",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", // JWT令牌
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```
- 失败(401 Unauthorized):
```json
{
  "error": "用户名或密码错误"
}
```

### 2. 用户登出

**请求**:
- 方法: POST
- URL: `/api/logout`
- Authorization: Bearer {access_token}

**响应**:
- 成功(200 OK):
```json
{
  "message": "登出成功"
}
```

### 3. 访问受保护资源

所有受保护的API端点都需要在请求头中包含JWT令牌：

**请求头**:
```
Authorization: Bearer {access_token}
```

**受保护的API端点包括**:
- `/api/test-auth` - 测试认证状态
- `/api/user/profile` - 获取和更新用户个人资料
- `/api/risk/assess` - 风险评估
- `/api/risk/history` - 查看评估历史

## 前端集成指南

### 1. 登录处理

```javascript
// 使用Fetch API示例
async function login(username, password) {
  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // 保存JWT令牌到本地存储
      localStorage.setItem('access_token', data.access_token);
      // 保存用户信息
      localStorage.setItem('user', JSON.stringify(data.user));
      
      return data;
    } else {
      throw new Error(data.error || '登录失败');
    }
  } catch (error) {
    console.error('登录错误:', error);
    throw error;
  }
}
```

### 2. 发送认证请求

创建一个包装函数来发送带JWT令牌的请求：

```javascript
// 带JWT认证的请求函数
async function authenticatedRequest(url, options = {}) {
  // 获取存储的JWT令牌
  const token = localStorage.getItem('access_token');
  
  // 设置默认headers
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  // 添加Authorization头
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  // 发送请求
  const response = await fetch(url, {
    ...options,
    headers
  });
  
  // 处理401错误（令牌过期或无效）
  if (response.status === 401) {
    // 清除无效令牌
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    // 重定向到登录页面
    window.location.href = '/login';
    throw new Error('认证失败，请重新登录');
  }
  
  return response;
}
```

### 3. 使用示例

```javascript
// 获取用户个人资料示例
async function getUserProfile() {
  try {
    const response = await authenticatedRequest('http://localhost:5000/api/user/profile', {
      method: 'POST'
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('用户资料:', data);
      return data;
    } else {
      throw new Error('获取用户资料失败');
    }
  } catch (error) {
    console.error('错误:', error);
    throw error;
  }
}

// 提交风险评估示例
async function submitRiskAssessment(assessmentData) {
  try {
    const response = await authenticatedRequest('http://localhost:5000/api/risk/assess', {
      method: 'POST',
      body: JSON.stringify(assessmentData)
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('评估结果:', data);
      return data;
    } else {
      throw new Error('提交评估失败');
    }
  } catch (error) {
    console.error('错误:', error);
    throw error;
  }
}
```

### 4. 自动登录状态检查

在应用初始化时检查用户登录状态：

```javascript
// 应用启动时检查登录状态
function checkAuthStatus() {
  const token = localStorage.getItem('access_token');
  const user = localStorage.getItem('user');
  
  if (token && user) {
    // 用户已登录
    return {
      isAuthenticated: true,
      user: JSON.parse(user)
    };
  } else {
    // 用户未登录
    return {
      isAuthenticated: false,
      user: null
    };
  }
}
```

## 注意事项

1. **令牌安全性**:
   - JWT令牌包含敏感信息，应妥善保管
   - 建议使用HTTPS协议传输令牌
   - 避免在URL中传递令牌

2. **令牌过期**:
   - 当前JWT令牌有效期为1小时
   - 令牌过期后需要重新登录
   - 前端应处理401错误，引导用户重新登录

3. **兼容性**:
   - 当前实现同时支持JWT认证和传统的Session认证
   - 这确保了在前端迁移期间的平稳过渡

4. **存储方式**:
   - 示例中使用localStorage存储令牌，也可以根据需要使用其他存储方式
   - 如果需要更高的安全性，可以考虑使用HttpOnly Cookie（需要后端配合设置）
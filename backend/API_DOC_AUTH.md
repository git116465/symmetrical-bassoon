# 糖尿病数据可视化系统 - 登录注册接口文档

## 项目概述

这是糖尿病数据可视化系统的登录注册相关接口文档，提供用户认证、个人信息管理等功能接口，方便前端开发人员进行对接。

## 基础URL

所有API的基础URL为：`http://localhost:5000`

## 认证相关接口

### 1. 用户注册

**请求URL**: `/api/register`

**请求方法**: POST

**请求体**: 
```json
{
  "username": "用户名",
  "email": "邮箱地址",
  "password": "密码"
}
```

**响应**: 
- 成功: `201 Created`
  ```json
  {"message": "注册成功"}
  ```
- 失败: `400 Bad Request`
  ```json
  {"error": "用户名已存在"} 或 {"error": "邮箱已存在"}
  ```

### 2. 用户登录

**请求URL**: `/api/login`

**请求方法**: POST

**请求体**: 
```json
{
  "username": "用户名",
  "password": "密码"
}
```

**响应**: 
- 成功: `200 OK`
  ```json
  {
    "message": "登录成功",
    "user": {
      "id": 用户ID,
      "username": "用户名",
      "email": "邮箱地址"
    }
  }
  ```
- 失败: `401 Unauthorized`
  ```json
  {"error": "用户名或密码错误"}
  ```

### 3. 用户登出

**请求URL**: `/api/logout`

**请求方法**: POST

**认证**: 需要登录

**响应**: 
```json
{"message": "登出成功"}
```

### 4. 获取/更新用户信息

**请求URL**: `/api/user/profile`

**请求方法**: GET (获取) / PUT (更新)

**认证**: 需要登录

**更新请求体**: 
```json
{
  "age": 年龄,
  "gender": "性别",
  "weight": 体重,
  "height": 身高,
  "family_history": 是否有家族病史
}
```

**获取响应**: 
```json
{
  "username": "用户名",
  "email": "邮箱地址",
  "age": 年龄,
  "gender": "性别",
  "weight": 体重,
  "height": 身高,
  "family_history": 是否有家族病史,
  "bmi": BMI值
}
```

**更新响应**: 
```json
{"message": "个人信息更新成功"}
```

## 风险评估接口

### 5. 评估糖尿病风险

**请求URL**: `/api/risk/assess`

**请求方法**: POST

**认证**: 需要登录

**请求体**（可选，不填则使用用户档案数据）: 
```json
{
  "age": 年龄,
  "gender": "性别",
  "bmi": BMI值,
  "family_history": 是否有家族病史
}
```

**响应**: 
```json
{
  "risk_score": 风险分数,
  "risk_level": "风险等级",
  "factors": {影响因素}
}
```

### 6. 获取风险评估历史

**请求URL**: `/api/risk/history`

**请求方法**: GET

**认证**: 需要登录

**响应**: 
```json
[
  {
    "id": 评估记录ID,
    "risk_score": 风险分数,
    "risk_level": "风险等级",
    "assessment_date": "评估日期",
    "factors": {影响因素}
  },
  ...
]
```

## 系统接口

### 7. 测试认证状态

**请求URL**: `/api/test-auth`

**请求方法**: GET

**认证**: 需要登录

**响应**: 
```json
{
  "message": "认证成功",
  "user": {
    "id": 用户ID,
    "username": "用户名",
    "email": "邮箱地址"
  }
}
```

### 8. 健康检查

**请求URL**: `/api/health`

**请求方法**: GET

**响应**: 
```json
{"status": "healthy", "service": "diabetes-visualization-api"}
```

## 开发注意事项

1. 所有需要认证的接口，请确保在请求头中包含session信息
2. 系统使用Flask-Login进行用户认证管理
3. 请处理好可能的错误情况，如网络异常、服务器错误等
4. 开发环境下，服务默认运行在 `http://localhost:5000`
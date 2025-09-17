# 糖尿病数据可视化系统 - 前端联调指南

## 概述

本文档提供了前端项目与糖尿病数据可视化系统后端API进行联调的详细指南，特别是针对前端项目位于不同电脑的情况。

## 后端网络配置

后端项目已配置以下关键参数，确保多机器环境下的联调：

1. **跨域支持**：已通过Flask-CORS配置，支持所有来源的跨域请求
2. **凭证支持**：`supports_credentials=True`，允许跨域传递认证信息
3. **监听地址**：绑定到`0.0.0.0`，允许从任何网络接口访问
4. **端口号**：`5000`

## 联调准备工作

### 1. 确认后端服务IP地址

在后端服务运行的电脑上，需要获取其局域网IP地址：

- **Windows系统**：打开命令提示符，输入`ipconfig`，查找"IPv4地址"（通常以192.168.x.x或10.x.x.x开头）
- **Mac/Linux系统**：打开终端，输入`ifconfig`或`ip addr`，查找本地IP地址

### 2. 确保网络连通性

在前端项目运行的电脑上，通过ping命令测试与后端服务的网络连通性：

```bash
ping [后端电脑IP地址]
```

如果ping不通，可能需要检查防火墙设置或网络配置。

## 前端项目配置

### 1. API基础URL设置

前端项目需要将API基础URL设置为后端服务的实际地址：

```javascript
// 例如：如果后端电脑IP为192.168.1.100
const API_BASE_URL = 'http://192.168.1.100:5000';
```

避免使用`localhost`或`127.0.0.1`，因为这些地址在前端项目运行的电脑上会指向自身而非后端服务。

### 2. 跨域请求配置

前端发送AJAX请求时，需要开启凭证支持：

#### Axios配置示例：

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://[后端IP]:5000',
  withCredentials: true, // 允许携带cookies
  headers: {
    'Content-Type': 'application/json'
  }
});
```

#### Fetch API配置示例：

```javascript
fetch('http://[后端IP]:5000/api/login', {
  method: 'POST',
  credentials: 'include', // 允许携带cookies
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({/* 请求数据 */})
});
```

### 3. 认证状态管理

- 登录成功后，后端会设置session cookie，前端后续请求会自动携带该cookie
- 前端需要实现认证状态检查，可以通过调用`/api/user/profile`接口判断用户是否已登录

## 常见问题及解决方案

### 1. 跨域请求被拒绝

**问题**：浏览器控制台显示CORS错误

**解决方案**：
- 确认后端已正确配置CORS（`CORS(app, supports_credentials=True)`）
- 检查前端请求是否开启了凭证支持
- 如使用自定义请求头，确保后端允许这些请求头

### 2. 无法连接到后端服务

**问题**：请求超时或连接被拒绝

**解决方案**：
- 确认后端服务正在运行（检查终端输出）
- 验证后端IP地址是否正确
- 检查防火墙设置，确保5000端口已开放
- 尝试使用telnet命令测试端口连通性：`telnet [后端IP] 5000`

### 3. 认证失败

**问题**：即使登录成功，后续请求仍返回未授权错误

**解决方案**：
- 确认前端请求已配置`withCredentials: true`或`credentials: 'include'`
- 检查浏览器cookie设置，确保允许第三方cookie
- 在开发环境中，可以考虑禁用浏览器的安全策略（仅用于开发测试）

## 开发调试技巧

### 1. 使用网络调试工具

- 浏览器开发者工具的Network面板，可以查看所有API请求的详细信息
- 推荐使用Postman或Insomnia等API测试工具，预先验证API功能

### 2. 后端日志查看

后端服务运行时会输出详细日志，可以查看请求处理情况和可能的错误信息。

### 3. 修改开发配置

如需调整后端服务配置，可以修改app.py文件中的相关参数：

```python
# 修改端口号
app.run(debug=True, host='0.0.0.0', port=8080)

# 调整CORS配置
CORS(app, origins=['http://frontend-ip:3000'], supports_credentials=True)
```

## 部署注意事项

在生产环境中，建议：

1. 使用反向代理（如Nginx）处理跨域问题
2. 配置HTTPS协议加密通信
3. 限制CORS允许的源，不使用通配符
4. 设置适当的安全头信息

---

如有其他联调问题，请联系后端开发人员协助解决。
# 糖尿病风险评估与数据可视化系统

## 项目简介
这是一个基于Flask开发的后端系统，提供糖尿病风险评估、用户认证和多维度数据可视化API。系统支持用户注册登录、风险评估、历史记录查询以及国内外糖尿病数据的多维度展示。

## 项目结构
```
f:\workspace\point\
├── app.py                 # 主应用文件，包含所有路由和业务逻辑
├── models.py              # 数据模型定义
├── config.py              # 应用配置文件
├── run.py                 # 应用启动脚本
├── requirements.txt       # 项目依赖列表
├── data/                  # 数据文件目录
│   ├── china_data.json    # 中国糖尿病数据
│   ├── international_data.json # 国际糖尿病数据
│   └── trends_data.json   # 趋势数据
├── utils/                 # 工具函数目录
│   ├── auth_decorator.py  # 认证装饰器
│   ├── data_loader.py     # 数据加载工具
│   └── risk_calculator.py # 风险评估计算器
├── instance/              # 实例目录（包含数据库）
│   └── database.db        # SQLite数据库文件
└── API_DOCUMENTATION.md   # API文档
```

## 环境要求
- Python 3.8+  
- pip 20.0+

## 安装步骤

### 1. 克隆项目（若从版本控制系统获取）
```bash
git clone <项目仓库地址>
cd point
```

### 2. 创建虚拟环境（推荐）

#### Windows系统
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

#### macOS/Linux系统
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖包
```bash
pip install -r requirements.txt
```

## 运行方法

### 开发模式运行
```bash
python run.py
```
或
```bash
flask run
```

系统将在 http://localhost:5000 启动开发服务器。

### 生产环境部署建议
对于生产环境，建议使用WSGI服务器如Gunicorn或uWSGI进行部署。

## 主要功能

1. **用户认证**
   - 用户注册、登录、注销
   - JWT令牌认证机制
   - 双认证模式支持

2. **糖尿病风险评估**
   - 基于多种健康因素的风险评分计算
   - 风险等级评估（低、中、高风险）
   - 个性化健康建议生成
   - 评估历史记录管理

3. **数据可视化API**
   - 中国糖尿病数据查询
   - 国际糖尿病数据查询
   - 趋势数据查询
   - 多维度数据分析（年龄分布、性别比例、地理分布等）

## API文档
详细的API文档请参考项目根目录下的以下文件：
- `API_DOCUMENTATION.md` - 主要API接口文档
- `API_DOC_AUTH.md` - 认证相关接口文档
- `API_DOC_CHINA.md` - 中国数据相关接口文档
- `API_DOC_INTERNATIONAL.md` - 国际数据相关接口文档
- `JWT_AUTH_API文档.md` - JWT认证详细文档

## 注意事项
1. 开发环境下默认启用调试模式，请在生产环境中关闭
2. 系统使用SQLite数据库，无需额外配置数据库服务
3. 项目已包含数据库文件(database.db)，其中包含示例数据
4. 若要清除所有数据，可直接删除database.db文件后重启应用，系统会自动创建新的数据库文件

## 开发指南
如需扩展功能，建议遵循以下流程：
1. 在models.py中定义新的数据模型
2. 在utils/目录下创建相应的工具函数
3. 在app.py中添加新的路由和业务逻辑
4. 更新requirements.txt以包含新的依赖
5. 完善相关API文档

## API使用示例
以下是一些常用API的简单使用示例：

### 1. 用户认证
```bash
# 用户注册
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123"}' http://localhost:5000/api/register

# 用户登录
curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123"}' http://localhost:5000/api/login
```

### 2. 风险评估
```bash
# 进行风险评估（需要认证）
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d '{"age":45,"gender":"male","family_history":true,"bmi":26.5,"physical_activity":"moderate","diet":"average","smoking":"never","alcohol":"rarely"}' http://localhost:5000/api/risk/assess
```

### 3. 数据查询
```bash
# 获取中国糖尿病数据
curl http://localhost:5000/china

# 获取国际糖尿病数据
curl http://localhost:5000/international
```

## 验证项目运行
成功启动项目后，您可以通过以下方式验证项目是否正常运行：
1. 访问 http://localhost:5000/api/health 检查系统健康状态
2. 使用上述API示例进行测试
3. 查看控制台输出，确保没有错误信息

## 数据说明
- 项目中包含的数据库文件(database.db)包含了示例用户数据和风险评估记录
- 数据目录(data/)下的JSON文件包含了用于可视化分析的中国、国际和趋势数据
- 风险评估算法位于utils/risk_calculator.py中，基于7个关键健康因素计算风险评分
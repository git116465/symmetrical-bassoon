# 糖尿病数据可视化系统 - 国际信息接口文档

## 项目概述

这是糖尿病数据可视化系统的国际信息相关接口文档，提供全球糖尿病数据查询、大洲/国家数据分析等功能接口，方便前端开发人员进行对接。

## 基础URL

所有API的基础URL为：`http://localhost:5000`

## 国际糖尿病数据接口

### 1. 获取国际糖尿病数据

**请求URL**: `/api/data/international`

**请求方法**: GET

**响应**: 国际糖尿病相关数据（详细结构请查看代码）

### 2. 获取详细国际数据

**请求URL**: `/api/data/international/detailed`

**请求方法**: GET

**响应**: 详细的国际国家/地区糖尿病数据

### 3. 获取特定大洲数据

**请求URL**: `/api/data/continents/<continent_name>`

**请求方法**: GET

**路径参数**: 
- `continent_name`: 大洲名称（如：亚洲、欧洲、北美洲等）

**响应**: 
```json
{
  "continent": "大洲名称",
  "countries": [国家数据列表],
  "summary": {
    "total_population": 总人口,
    "total_cases": 总病例数,
    "avg_rate": 平均患病率
  }
}
```

### 4. 获取特定国家数据

**请求URL**: `/api/data/countries/<country_name>`

**请求方法**: GET

**路径参数**: 
- `country_name`: 国家名称

**响应**: 
```json
{
  "country": "国家名称",
  "population": 人口,
  "cases": 病例数,
  "prevalence_rate": 患病率,
  "year": 数据年份,
  "factors": {影响因素}
}
```

## 数据可视化接口（适用于国际数据）

### 5. 获取大洲数据（柱状图）

**请求URL**: `/api/continents-data`

**请求方法**: GET

**响应**: 
```json
{
  "xAxis": ["大洲1", "大洲2", ...],
  "seriesData": [患病率1, 患病率2, ...]
}
```

### 6. 获取国家数据（地图）

**请求URL**: `/api/countries-data`

**请求方法**: GET

**响应**: 
```json
[
  {"name": "国家名称", "value": 患病率, "continent": "大洲名称"},
  ...
]
```

### 7. 获取地理分布数据（地图）

**请求URL**: `/api/geo-distribution`

**请求方法**: GET

**响应**: 
```json
{
  "mapData": [
    {"name": "国家名称", "value": 患病率},
    ...
  ]
}
```

## 系统接口

### 8. 健康检查

**请求URL**: `/api/health`

**请求方法**: GET

**响应**: 
```json
{"status": "healthy", "service": "diabetes-visualization-api"}
```

## 开发注意事项

1. 请处理好可能的错误情况，如网络异常、服务器错误等
2. 开发环境下，服务默认运行在 `http://localhost:5000`
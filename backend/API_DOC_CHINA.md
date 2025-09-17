# 糖尿病数据可视化系统 - 国内信息接口文档

## 项目概述

这是糖尿病数据可视化系统的国内信息相关接口文档，提供中国糖尿病数据查询、区域数据分析等功能接口，方便前端开发人员进行对接。

## 基础URL

所有API的基础URL为：`http://localhost:5000`

## 中国糖尿病数据接口

### 1. 获取中国糖尿病数据

**请求URL**: `/api/data/china`

**请求方法**: GET

**响应**: 中国糖尿病相关数据（详细结构请查看代码）

### 2. 获取详细中国数据

**请求URL**: `/api/data/china/detailed`

**请求方法**: GET

**响应**: 详细的中国省份糖尿病数据

### 3. 获取特定区域数据

**请求URL**: `/api/data/regions/<region_name>`

**请求方法**: GET

**路径参数**: 
- `region_name`: 区域名称

**响应**: 
```json
{
  "region": "区域名称",
  "provinces": [省份数据列表],
  "summary": {
    "total_population": 总人口,
    "total_cases": 总病例数,
    "avg_rate": 平均患病率
  }
}
```

### 4. 获取糖尿病并发症数据

**请求URL**: `/api/data/complications`

**请求方法**: GET

**响应**: 
```json
{
  "complications": [
    {"name": "并发症名称", "prevalence": 患病率, "severity": "严重程度"},
    ...
  ]
}
```

## 数据可视化接口（适用于中国数据）

### 5. 获取年龄分布数据（柱状图）

**请求URL**: `/api/age-distribution`

**请求方法**: GET

**响应**: 
```json
{
  "xAxis": ["年龄范围1", "年龄范围2", ...],
  "seriesData": [患病率1, 患病率2, ...]
}
```

### 6. 获取性别比例数据（饼图）

**请求URL**: `/api/gender-ratio`

**请求方法**: GET

**响应**: 
```json
[
  {"name": "男性", "value": 比例值},
  {"name": "女性", "value": 比例值}
]
```

### 7. 获取血糖趋势数据（折线图）

**请求URL**: `/api/blood-sugar-trend`

**请求方法**: GET

**响应**: 
```json
{
  "xAxis": ["年份1", "年份2", ...],
  "seriesData": [患病率1, 患病率2, ...]
}
```

### 8. 获取健康提示信息

**请求URL**: `/api/health-tips`

**请求方法**: GET

**响应**: 
```json
[
  "健康提示1",
  "健康提示2",
  ...
]
```

## 省份数据接口

### 9. 获取所有省份基础数据（用于地图）

**请求URL**: `/api/provinces/data`

**请求方法**: GET

**响应**: 
```json
[
  {"name": "北京", "value": 0.1328},
  {"name": "上海", "value": 0.216},
  {"name": "广东", "value": 0.13},
  // ... 其他省份
]
```

### 10. 获取特定省份详细数据

**请求URL**: `/api/provinces/{province}/details`

**请求方法**: GET

**路径参数**: 
- `province`: 省份名称

**响应**: 
```json
{
  "province": "北京",
  "ageDistribution": {
    "ranges": ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"],
    "values": [2.8, 6.2, 12.8, 20.5, 26.0, 29.5]
  },
  "genderRatio": [
    {"value": 54, "name": "男性"},
    {"value": 46, "name": "女性"}
  ],
  "bloodSugarTrend": {
    "years": ["2019", "2020", "2021", "2022", "2023"],
    "values": [12.8, 13.0, 13.1, 13.2, 13.3]
  }
}
```

### 11. 获取全国汇总数据

**请求URL**: `/api/provinces/national-summary`

**请求方法**: GET

**响应**: 
```json
{
  "summary": {
    "average_rate": 8.8,
    "total_population": 1400000000,
    "total_cases": 123200000,
    "provinces_count": 34
  },
  "ageDistribution": {
    "ranges": ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"],
    "values": [2.8, 6.2, 12.8, 20.5, 26.0, 29.5]
  },
  "genderRatio": [
    {"value": 51, "name": "男性"},
    {"value": 49, "name": "女性"}
  ],
  "bloodSugarTrend": {
    "years": ["2019", "2020", "2021", "2022", "2023"],
    "values": [8.8, 9.0, 9.2, 9.5, 9.8]
  }
}
```

## 系统接口

### 12. 健康检查

**请求URL**: `/api/health`

**请求方法**: GET

**响应**: 
```json
{"status": "healthy", "service": "diabetes-visualization-api"}
```

## 开发注意事项

1. 请处理好可能的错误情况，如网络异常、服务器错误等
2. 开发环境下，服务默认运行在 `http://localhost:5000`
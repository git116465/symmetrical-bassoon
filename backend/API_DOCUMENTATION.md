# 糖尿病风险评估系统 API 文档

## 数据可视化相关接口

### 1. 趋势数据接口

**URL**: `/api/data/trends/simple`

**方法**: `GET`

**认证要求**: 不需要登录

**请求参数**: 无

**响应**: JSON 格式，包含趋势数据

| 字段 | 类型 | 描述 |
|------|------|------|
| `years` | array | 年份数组 |
| `prevalence` | array | 患病率数组 (百分比) |
| `source` | string | 数据来源 |
| `last_updated` | string | 最后更新日期 |

**响应示例**:
```json
{
  "years": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022],
  "prevalence": [4.7, 5.5, 6.2, 6.9, 7.8, 8.4, 9.2, 9.8],
  "source": "国际糖尿病联盟",
  "last_updated": "2023-11-15"
}
```

# API接口文档

## 风险评估接口

### 1. 评估糖尿病风险

**接口地址**: `/api/risk/assess`

**请求方法**: POST

**认证要求**: 无（未登录用户可直接测评）

**请求体参数**: JSON格式

```json
{
  "age_range": "string", // 必填，年龄范围，可选值："20-39", "40-49", "50-59", "60-69", "70+"
  "bmi_category": "string", // 必填，BMI分类，可选值："underweight", "normal", "overweight", "obese"
  "waist_status": "string", // 必填，腰围状态，可选值："normal-male", "normal-female", "abnormal-male", "abnormal-female"
  "family_history": "string", // 必填，家族病史，可选值："yes", "no"
  "physical_activity": "string", // 必填，运动频率，可选值："regular", "irregular", "sedentary"
  "blood_pressure": "string", // 必填，高血压状况，可选值："yes", "no"
  "glucose_history": "string" // 必填，血糖异常史，可选值："yes", "no"
}
```

**响应参数**: JSON格式

```json
{
  "risk_score": number, // 风险评分（0-22分）
  "risk_percentage": number, // 风险百分比（0-100%）
  "risk_level": "string", // 风险等级，可能值："low", "medium", "high"
  "risk_factors": object, // 各项风险因素的详细信息
  "suggestions": ["string"], // 个性化健康建议
  "assessment_date": "string" // 评估时间（ISO格式）
}
```

**错误响应**: JSON格式，HTTP状态码400或500

```json
{
  "error": "错误描述信息"
}
```

### 2. 获取风险评估历史

**接口地址**: `/api/risk/history`

**请求方法**: GET

**认证要求**: 需要登录（使用dual_auth_required装饰器）

**请求参数**: 无

**响应参数**: JSON格式

```json
[
  {
    "id": number, // 评估记录ID
    "risk_score": number, // 风险评分
    "risk_level": "string", // 风险等级
    "factors": object, // 风险因素
    "assessment_date": "string" // 评估时间
  }
  // 更多评估记录...
]
```


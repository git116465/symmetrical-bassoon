import json

def calculate_risk_score(data):
    """
    根据用户数据计算糖尿病风险评分
    新算法支持7个输入字段：age_range, bmi_category, waist_status, 
    family_history, physical_activity, blood_pressure, glucose_history
    """
    risk_score = 0
    factors = {}
    
    # 年龄评分
    age_scores = {
        "20-39": 0, "40-49": 2, "50-59": 3,
        "60-69": 4, "70+": 5
    }
    age_range = data.get('age_range', '20-39')
    age_score = age_scores.get(age_range, 0)
    risk_score += age_score
    factors['age'] = {
        'score': age_score,
        'description': age_range + '岁'
    }
    
    # BMI评分
    bmi_scores = {
        "underweight": 0, "normal": 1,
        "overweight": 3, "obese": 5
    }
    bmi_category = data.get('bmi_category', 'normal')
    bmi_score = bmi_scores.get(bmi_category, 0)
    risk_score += bmi_score
    factors['bmi'] = {
        'score': bmi_score,
        'description': get_bmi_description(bmi_category)
    }
    
    # 腰围状态评分
    waist_scores = {
        "normal-male": 0, "normal-female": 0,
        "abnormal-male": 3, "abnormal-female": 3
    }
    waist_status = data.get('waist_status', 'normal-male')
    waist_score = waist_scores.get(waist_status, 0)
    risk_score += waist_score
    factors['waist'] = {
        'score': waist_score,
        'description': '腰围正常' if 'normal' in waist_status else '腰围异常'
    }
    
    # 家族病史评分
    family_history = data.get('family_history', 'no')
    family_score = 3 if family_history == 'yes' else 0
    risk_score += family_score
    factors['family'] = {
        'score': family_score,
        'description': '有家族病史' if family_history == 'yes' else '无家族病史'
    }
    
    # 运动频率评分
    activity_scores = {
        "regular": 0, "irregular": 2, "sedentary": 4
    }
    physical_activity = data.get('physical_activity', 'regular')
    activity_score = activity_scores.get(physical_activity, 0)
    risk_score += activity_score
    factors['activity'] = {
        'score': activity_score,
        'description': get_activity_description(physical_activity)
    }
    
    # 高血压评分
    blood_pressure = data.get('blood_pressure', 'no')
    bp_score = 3 if blood_pressure == 'yes' else 0
    risk_score += bp_score
    factors['blood_pressure'] = {
        'score': bp_score,
        'description': '有高血压' if blood_pressure == 'yes' else '无高血压'
    }
    
    # 血糖异常史评分
    glucose_history = data.get('glucose_history', 'no')
    glucose_score = 5 if glucose_history == 'yes' else 0
    risk_score += glucose_score
    factors['glucose'] = {
        'score': glucose_score,
        'description': '有血糖异常史' if glucose_history == 'yes' else '无血糖异常史'
    }
    
    # 确定风险等级和百分比
    risk_level, risk_percentage = determine_risk_level(risk_score)
    
    # 生成个性化建议
    suggestions = generate_suggestions(factors, risk_level)
    
    return {
        'risk_score': risk_score,
        'risk_percentage': risk_percentage,
        'risk_level': risk_level,
        'risk_factors': factors,
        'suggestions': suggestions
    }

def get_bmi_description(bmi_category):
    """获取BMI分类的中文描述"""
    descriptions = {
        "underweight": "偏瘦",
        "normal": "正常",
        "overweight": "超重",
        "obese": "肥胖"
    }
    return descriptions.get(bmi_category, bmi_category)

def get_activity_description(activity_level):
    """获取运动频率的中文描述"""
    descriptions = {
        "regular": "规律运动",
        "irregular": "运动不规律",
        "sedentary": "久坐不动"
    }
    return descriptions.get(activity_level, activity_level)

def determine_risk_level(score):
    """根据评分确定风险等级和百分比"""
    if score >= 17:
        return 'high', min(95 + (score - 17) * 1, 100)
    elif score >= 10:
        return 'medium', 40 + (score - 10) * 5
    else:
        return 'low', min(20 + score * 2, 39)

def generate_suggestions(factors, risk_level):
    """根据风险因素和等级生成个性化建议"""
    suggestions = []
    
    # 基于BMI的建议
    if factors.get('bmi', {}).get('score', 0) >= 3:
        suggestions.append("控制饮食，减少热量摄入，增加蔬菜和水果的比例")
        suggestions.append("在医生指导下制定科学的减重计划")
    
    # 基于腰围的建议
    if factors.get('waist', {}).get('score', 0) > 0:
        suggestions.append("避免久坐，定期起身活动")
        suggestions.append("增加腹部锻炼，如平板支撑、仰卧起坐等")
    
    # 基于运动的建议
    if factors.get('activity', {}).get('score', 0) > 0:
        suggestions.append("增加运动量，每周至少进行150分钟中等强度有氧运动")
        suggestions.append("选择适合自己的运动方式，如快走、游泳、骑自行车等")
    
    # 基于高血压的建议
    if factors.get('blood_pressure', {}).get('score', 0) > 0:
        suggestions.append("减少盐的摄入，每天不超过5克")
        suggestions.append("定期监测血压，如有需要及时就医")
    
    # 基于血糖异常史的建议
    if factors.get('glucose', {}).get('score', 0) > 0:
        suggestions.append("定期检测血糖，遵医嘱进行治疗")
        suggestions.append("避免高糖食物，选择低GI食物")
    
    # 通用建议
    if not suggestions:
        suggestions.append("保持健康的生活方式，均衡饮食，适量运动")
        suggestions.append("定期体检，关注血糖变化")
    
    # 根据风险等级调整建议
    if risk_level == 'high':
        suggestions.append("建议尽快咨询医生，进行全面的健康检查")
    elif risk_level == 'medium':
        suggestions.append("建议3-6个月内进行一次血糖检测")
    
    # 限制建议数量
    return suggestions[:5]
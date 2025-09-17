import json
import pandas as pd
from typing import List, Dict

def process_province_data() -> List[Dict]:
    """
    从Excel数据中提取省份糖尿病信息
    """
    # 这是从Excel中提取的结构化数据
    province_data = [
        {"name": "黑龙江", "male_rate": 14.47, "female_rate": 10.49, "total_rate": 12.34, "population": 3125, "cases": 385, "summary": "已有糖尿病患者近400万，每10人中就有1人患有糖尿病，已成为糖尿病高发地区。"},
        {"name": "吉林", "male_rate": 14.73, "female_rate": 12.55, "total_rate": 15.8, "population": 2407, "cases": 380, "summary": "男性更高的吸烟率，快速增长的肥胖率，以及社会文化和生物学因素"},
        {"name": "辽宁", "male_rate": 17.4, "female_rate": 18.46, "total_rate": 17.96, "population": 4259, "cases": 765, "summary": "女性、高年龄、高学历、城市、吸烟、饮酒、超重、肥胖、高血压、血脂异常、职业(除农民)均为糖尿病的危险因素"},
        {"name": "内蒙古", "male_rate": 16.1, "female_rate": 12.5, "total_rate": 15.5, "population": 2405, "cases": 373, "summary": "内蒙古糖尿病患病率随时间推移呈上升趋势"},
        {"name": "新疆", "male_rate": 13.65, "female_rate": 10.04, "total_rate": 10.4, "population": 2585, "cases": 269, "summary": "糖尿病患病率及空腹血糖受损率随着年龄的增加而升高"},
        {"name": "甘肃", "male_rate": 12.3, "female_rate": 9.2, "total_rate": 10.6, "population": 2502, "cases": 265, "summary": "甘肃省糖尿病患病率较高且呈增长趋势，这需要引起高度重视"},
        {"name": "宁夏", "male_rate": 5.2, "female_rate": 4.8, "total_rate": 5.0, "population": 725, "cases": 36, "summary": "只统计了2型糖尿病的患病率，逐年增长的趋势"},
        {"name": "陕西", "male_rate": 29.4, "female_rate": 24.5, "total_rate": 26.3, "population": 3954, "cases": 1040, "summary": "只统计了35岁以上人群的患病率，关中地区显著高于关南地区"},
        {"name": "山西", "male_rate": 5.8, "female_rate": 4.85, "total_rate": 5.27, "population": 3492, "cases": 184, "summary": "饮食以面食等碳水化合物为主，且存在食用油、食盐摄入量超标，吸烟、过量饮酒、身体活动不足等不健康生活方式有关"},
        {"name": "河北", "male_rate": 13.1, "female_rate": 12.8, "total_rate": 12.9, "population": 7556, "cases": 975, "summary": "河北省的糖尿病患病率较高，且在不同年龄、城乡之间存在着差异"},
        {"name": "北京", "male_rate": 13.66, "female_rate": 12.91, "total_rate": 13.28, "population": 2154, "cases": 286, "summary": "虽然城市和农村地区的糖尿病患病率都在增加，但城市地区的患病率通常高于农村"},
        {"name": "天津", "male_rate": 14.73, "female_rate": 12.55, "total_rate": 20.0, "population": 1387, "cases": 277, "summary": "天津市糖尿病患病率随着年龄的增加而上升，尤其在40岁以上人群中患病率显著增加"},
        {"name": "山东", "male_rate": None, "female_rate": None, "total_rate": 10.3, "population": 10153, "cases": 1046, "summary": "近年来患病率持续升高，45岁以后更为显著，但近年未有权威数据展现男女患病概率"},
        {"name": "河南", "male_rate": None, "female_rate": None, "total_rate": 9.96, "population": 9937, "cases": 990, "summary": "近年来未有权威数据展现男女患病概率"},
        {"name": "青海", "male_rate": 8.77, "female_rate": 6.22, "total_rate": 7.39, "population": 603, "cases": 45, "summary": "青海省的糖尿病患病率虽然相对较低，但呈现出增长趋势，并在不同年龄、城乡和民族间存在差异"},
        {"name": "西藏", "male_rate": 4.56, "female_rate": 2.33, "total_rate": 6.8, "population": 366, "cases": 25, "summary": "西藏自治区的糖尿病患病率虽然仍低于一些经济发达地区，但增长趋势明显"},
        {"name": "四川", "male_rate": 14.73, "female_rate": 12.55, "total_rate": 12.94, "population": 8375, "cases": 1084, "summary": "四川省属于西南地区，糖尿病患病率增速较快"},
        {"name": "重庆", "male_rate": None, "female_rate": None, "total_rate": 17.9, "population": 3212, "cases": 575, "summary": "重庆市的糖尿病患病率较高，且在不同年龄、城乡和性别间存在差异"},
        {"name": "湖北", "male_rate": 9.79, "female_rate": 6.69, "total_rate": 8.26, "population": 5830, "cases": 482, "summary": "糖尿病患病率与年龄密切相关，随年龄增长而升高"},
        {"name": "安徽", "male_rate": 6.8, "female_rate": 5.4, "total_rate": 6.1, "population": 6324, "cases": 386, "summary": "2013年统计数据，近年来有增长但无具体数据"},
        {"name": "江苏", "male_rate": 8.6, "female_rate": 8.4, "total_rate": 8.5, "population": 8475, "cases": 720, "summary": "男性可能更倾向于高热量饮食、缺乏运动，女性由于生理周期、妊娠和更年期等生理因素，可能对糖尿病的易感性有所不同"},
        {"name": "浙江", "male_rate": 8.36, "female_rate": 9.13, "total_rate": 8.77, "population": 6540, "cases": 574, "summary": "随着时间的推移和生活方式的改变，浙江省糖尿病的患病率可能会有所变化"},
        {"name": "上海", "male_rate": None, "female_rate": None, "total_rate": 21.6, "population": 2428, "cases": 525, "summary": "35岁以上的常驻居民数据"},
        {"name": "江西", "male_rate": 8.2, "female_rate": 7.2, "total_rate": 6.69, "population": 4519, "cases": 302, "summary": "男女分别数据为2010年统计，总数据为2018年统计"},
        {"name": "湖南", "male_rate": 14.8, "female_rate": 18.3, "total_rate": 8.9, "population": 6644, "cases": 591, "summary": "统计数据为2014年，男女数据为60岁及以上的患病率，总体数据为18岁以上"},
        {"name": "贵州", "male_rate": 8.8, "female_rate": 6.5, "total_rate": 7.6, "population": 3856, "cases": 293, "summary": "统计数据为2015年，18岁以上人群患病率"},
        {"name": "云南", "male_rate": None, "female_rate": None, "total_rate": 7.1, "population": 4830, "cases": 343, "summary": "处于中等水平，无权威数据展示男女患病率"},
        {"name": "广西", "male_rate": None, "female_rate": None, "total_rate": 7.1, "population": 5013, "cases": 356, "summary": "数据为2010年，无权威数据展示男女患病率"},
        {"name": "广东", "male_rate": None, "female_rate": None, "total_rate": 13.0, "population": 12601, "cases": 1638, "summary": "数据为2013年统计，18岁以上人群患病率"},
        {"name": "海南", "male_rate": 11.7, "female_rate": 7.9, "total_rate": 12.0, "population": 1020, "cases": 122, "summary": "男性、受教育程度低、超重和肥胖、有糖尿病家族史人群总糖尿病患病率较高，18岁及以上人群"}
    ]
    
    return province_data

def generate_china_data_json():
    """
    生成完整的china_data.json文件
    """
    provinces = process_province_data()
    
    # 构建完整的JSON结构
    china_data = {
        "metadata": {
            "data_source": "省份.xlsx",
            "last_updated": "2025-07-15",
            "total_provinces": len(provinces),
            "rate_unit": "percentage",
            "population_unit": "万人"
        },
        "summary": {
            "total_population": sum(province["population"] for province in provinces),
            "total_cases": sum(province["cases"] for province in provinces),
            "avg_diabetes_rate": round(sum(province["total_rate"] for province in provinces if province["total_rate"] is not None) / 
                                      len([p for p in provinces if p["total_rate"] is not None]), 2)
        },
        "provinces": provinces,
        "regions": {
            "northeast": ["黑龙江", "吉林", "辽宁"],
            "north": ["北京", "天津", "河北", "山西", "内蒙古"],
            "east": ["上海", "江苏", "浙江", "安徽", "福建", "江西", "山东"],
            "central": ["河南", "湖北", "湖南"],
            "south": ["广东", "广西", "海南"],
            "southwest": ["重庆", "四川", "贵州", "云南", "西藏"],
            "northwest": ["陕西", "甘肃", "青海", "宁夏", "新疆"]
        }
    }
    
    # 保存为JSON文件
    with open('data/china_data.json', 'w', encoding='utf-8') as f:
        json.dump(china_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 china_data.json")
    print(f"📊 包含 {len(provinces)} 个省份数据")
    print(f"👥 总人口: {china_data['summary']['total_population']} 万人")
    print(f"🩺 总病例数: {china_data['summary']['total_cases']} 万人")
    print(f"📈 平均患病率: {china_data['summary']['avg_diabetes_rate']}%")
    
    return china_data

def create_data_loader_update():
    """
    更新数据加载器以支持新格式
    """
    loader_code = '''
import json
import os

def load_china_data():
    """加载中国省份糖尿病数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'china_data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 为前端提供简化格式
            simplified_provinces = []
            for province in data['provinces']:
                simplified_provinces.append({
                    'name': province['name'],
                    'diabetes_rate': province['total_rate'],
                    'population': province['population'],
                    'cases': province['cases'],
                    'male_rate': province['male_rate'],
                    'female_rate': province['female_rate']
                })
            
            return {
                'provinces': simplified_provinces,
                'metadata': data['metadata'],
                'summary': data['summary'],
                'regions': data['regions']
            }
            
    except FileNotFoundError:
        # 返回示例数据
        return {
            "provinces": [
                {"name": "北京", "diabetes_rate": 8.5, "population": 2154, "cases": 183},
                {"name": "上海", "diabetes_rate": 9.2, "population": 2428, "cases": 223},
            ],
            "metadata": {
                "data_source": "fallback",
                "last_updated": "2025-07-15"
            }
        }
'''

    with open('utils/data_loader.py', 'w', encoding='utf-8') as f:
        f.write(loader_code)
    
    print("✅ 已更新数据加载器")

if __name__ == "__main__":
    # 生成数据文件
    generate_china_data_json()
    
    # 更新数据加载器
    create_data_loader_update()
    
    print("\n🎉 所有文件已生成完成！")
    print("📁 china_data.json 已保存到 data/ 目录")
    print("📁 data_loader.py 已更新")
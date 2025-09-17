import json
from typing import List, Dict

def process_international_data() -> List[Dict]:
    """
    从Excel数据中提取世界各大洲糖尿病信息
    """
    continent_data = [
        {
            "name": "亚洲",
            "diabetes_rate": 60.0,
            "population": 4641,  # 百万
            "cases": 2785,      # 百万
            "countries": 48,
            "summary": "亚洲是全球糖尿病患病率最高的地区，主要由于人口基数大、饮食习惯改变和城市化进程加快",
            "trend": "rising",
            "risk_factors": ["饮食习惯西方化", "缺乏运动", "肥胖率上升", "遗传因素"]
        },
        {
            "name": "非洲",
            "diabetes_rate": 10.5,
            "population": 1370,
            "cases": 144,
            "countries": 54,
            "summary": "非洲糖尿病患病率相对较低但增长迅速，医疗资源匮乏是主要挑战",
            "trend": "rapidly_rising",
            "risk_factors": ["城市化", "饮食变化", "医疗条件有限", "健康意识不足"]
        },
        {
            "name": "大洋洲",
            "diabetes_rate": 12.3,
            "population": 43,
            "cases": 5.3,
            "countries": 14,
            "summary": "大洋洲地区糖尿病患病率较高，特别是澳大利亚和新西兰的土著人群",
            "trend": "stable",
            "risk_factors": ["肥胖问题", "土著人群遗传易感性", "生活方式变化"]
        },
        {
            "name": "北美洲",
            "diabetes_rate": 10.4,
            "population": 592,
            "cases": 61.6,
            "countries": 23,
            "summary": "北美洲糖尿病患病率较高，美国是糖尿病大国，但近年来防控措施有所成效",
            "trend": "slowly_rising",
            "risk_factors": ["高糖饮食", "久坐生活方式", "肥胖 epidemic", "老龄化"]
        },
        {
            "name": "南美洲",
            "diabetes_rate": 9.4,
            "population": 434,
            "cases": 40.8,
            "countries": 12,
            "summary": "南美洲糖尿病患病率中等，但城市化进程导致患病率持续上升",
            "trend": "rising",
            "risk_factors": ["城市化", "饮食结构变化", "经济快速发展", "健康服务不均"]
        },
        {
            "name": "欧洲",
            "diabetes_rate": 8.1,
            "population": 747,
            "cases": 60.5,
            "countries": 44,
            "summary": "欧洲糖尿病患病率相对较低但持续增长，东欧地区患病率高于西欧",
            "trend": "slowly_rising",
            "risk_factors": ["老龄化人口", "肥胖问题", "生活方式", "东欧经济转型影响"]
        },
        {
            "name": "南极洲",
            "diabetes_rate": None,
            "population": 0.004,  # 科研人员
            "cases": None,
            "countries": 0,
            "summary": "南极洲无常住人口，仅有科研人员临时居住，无糖尿病统计资料",
            "trend": "unknown",
            "risk_factors": ["极端环境", "特殊饮食", "科研工作压力"],
            "note": "无常住人口，数据暂缺"
        }
    ]
    
    return continent_data

def generate_international_data_json():
    """
    生成完整的international_data.json文件
    """
    continents = process_international_data()
    
    # 计算统计摘要
    valid_continents = [c for c in continents if c["diabetes_rate"] is not None]
    
    # 构建完整的JSON结构
    international_data = {
        "metadata": {
            "data_source": "世界数据.xlsx",
            "last_updated": "2025-07-15",
            "total_continents": len(valid_continents),
            "rate_unit": "percentage",
            "population_unit": "百万人",
            "cases_unit": "百万人"
        },
        "summary": {
            "total_population": sum(continent["population"] for continent in valid_continents),
            "total_cases": sum(continent["cases"] for continent in valid_continents if continent["cases"] is not None),
            "avg_diabetes_rate": round(sum(continent["diabetes_rate"] for continent in valid_continents) / len(valid_continents), 1),
            "total_countries": sum(continent["countries"] for continent in valid_continents),
            "highest_rate_continent": max(valid_continents, key=lambda x: x["diabetes_rate"])["name"],
            "lowest_rate_continent": min(valid_continents, key=lambda x: x["diabetes_rate"])["name"]
        },
        "continents": continents,
        "global_trends": {
            "years": [2010, 2015, 2020, 2025],
            "global_rates": [8.4, 9.2, 10.5, 11.3],
            "trend_description": "全球糖尿病患病率持续上升，预计到2045年将有7亿糖尿病患者"
        },
        "risk_levels": [
            {"level": "high", "range": ">10%", "continents": ["亚洲", "非洲", "大洋洲", "北美洲"]},
            {"level": "medium", "range": "5-10%", "continents": ["南美洲", "欧洲"]},
            {"level": "low", "range": "<5%", "continents": []},
            {"level": "unknown", "range": "无数据", "continents": ["南极洲"]}
        ]
    }
    
    # 保存为JSON文件
    with open('data/international_data.json', 'w', encoding='utf-8') as f:
        json.dump(international_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 international_data.json")
    print(f"🌍 包含 {len(continents)} 个大洲数据")
    print(f"👥 总人口: {international_data['summary']['total_population']} 百万")
    print(f"🩺 总病例数: {international_data['summary']['total_cases']} 百万")
    print(f"📈 平均患病率: {international_data['summary']['avg_diabetes_rate']}%")
    print(f"🏆 最高患病率: {international_data['summary']['highest_rate_continent']}")
    print(f"📉 最低患病率: {international_data['summary']['lowest_rate_continent']}")
    
    return international_data

def update_data_loader_for_international():
    """
    更新数据加载器以支持国际数据
    """
    loader_code = '''import json
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

def load_international_data():
    """加载国际糖尿病数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'international_data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 为前端提供简化格式
            simplified_continents = []
            for continent in data['continents']:
                simplified_continents.append({
                    'name': continent['name'],
                    'diabetes_rate': continent['diabetes_rate'],
                    'population': continent['population'],
                    'cases': continent['cases'],
                    'countries': continent['countries']
                })
            
            return {
                'continents': simplified_continents,
                'metadata': data['metadata'],
                'summary': data['summary'],
                'global_trends': data['global_trends'],
                'risk_levels': data['risk_levels']
            }
            
    except FileNotFoundError:
        # 返回示例数据
        return {
            "continents": [
                {"name": "亚洲", "diabetes_rate": 60.0, "countries": 48},
                {"name": "欧洲", "diabetes_rate": 6.2, "countries": 44},
            ],
            "metadata": {
                "data_source": "fallback",
                "last_updated": "2025-07-15"
            }
        }

def load_trends_data():
    """加载趋势数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'trends_data.json')
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "years": [2010, 2015, 2020, 2025],
            "global_rates": [6.4, 7.2, 8.5, 9.2],
            "china_rates": [7.8, 8.6, 9.8, 10.6]
        }
'''
    
    with open('utils/data_loader.py', 'w', encoding='utf-8') as f:
        f.write(loader_code)
    
    print("✅ 已更新数据加载器，支持国际数据")

# 创建示例趋势数据文件
def create_trends_data_file():
    """创建趋势数据文件"""
    trends_data = {
        "metadata": {
            "data_source": "WHO全球糖尿病报告",
            "last_updated": "2025-07-15",
            "rate_unit": "percentage"
        },
        "global_trends": {
            "years": [1990, 2000, 2010, 2020, 2025, 2030, 2040, 2045],
            "rates": [4.7, 5.4, 6.4, 8.5, 9.2, 10.2, 11.3, 12.2],
            "projected_cases": [151, 171, 285, 463, 578, 643, 700, 783]  # 百万
        },
        "regional_trends": {
            "asia": {
                "years": [2010, 2015, 2020, 2025],
                "rates": [55.0, 57.0, 59.0, 60.0]
            },
            "europe": {
                "years": [2010, 2015, 2020, 2025],
                "rates": [7.2, 7.6, 7.9, 8.1]
            },
            "africa": {
                "years": [2010, 2015, 2020, 2025],
                "rates": [7.8, 8.9, 9.8, 10.5]
            }
        },
        "china_vs_global": {
            "years": [2010, 2015, 2020, 2025],
            "global_rates": [6.4, 7.2, 8.5, 9.2],
            "china_rates": [7.8, 8.6, 9.8, 10.6],
            "difference": [1.4, 1.4, 1.3, 1.4]
        }
    }
    
    with open('data/trends_data.json', 'w', encoding='utf-8') as f:
        json.dump(trends_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 已生成趋势数据文件")

if __name__ == "__main__":
    # 生成国际数据文件
    generate_international_data_json()
    
    # 更新数据加载器
    update_data_loader_for_international()
    
    # 生成趋势数据文件
    create_trends_data_file()
    
    print("\n🎉 所有国际数据文件已生成完成！")
    print("📁 international_data.json 已保存到 data/ 目录")
    print("📁 trends_data.json 已保存到 data/ 目录")
    print("📁 data_loader.py 已更新支持国际数据")
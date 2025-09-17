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

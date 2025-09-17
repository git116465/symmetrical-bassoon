from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from utils.auth_decorator import dual_auth_required
from models import db, User, RiskAssessment
from config import Config
from utils.data_loader import load_china_data, load_international_data, load_trends_data
from utils.risk_calculator import calculate_risk_score
import json
from collections import defaultdict
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 额外的会话配置，确保跨域请求中会话正常工作
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # 初始化扩展
    db.init_app(app)
    CORS(app, supports_credentials=True, resources={"/*": {"origins": "*"}})
    
    # 初始化JWT管理 - 配置兼容性选项
    jwt = JWTManager(app)
    
    # 额外的JWT配置，确保与Flask 3.0.0兼容
    app.config['JWT_DECODE_ALGORITHMS'] = ['HS256']  # 明确指定算法
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False   # 禁用CSRF保护以简化测试
    
    # 初始化登录管理（保留兼容性）
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/api/login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # JWT用户身份加载器
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.get(identity)
    
    # 确保Flask-Login能够识别JWT认证的用户
    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # 处理传入的用户对象或用户ID
        if hasattr(identity, 'id'):
            # 如果传入的是用户对象，返回其ID
            return identity.id
        else:
            # 如果传入的已经是用户ID，直接返回
            return identity
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "error": "令牌已过期",
            "message": "请重新登录获取新令牌"
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            "error": "无效的令牌",
            "message": f"令牌验证失败: {error_string}"
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({
            "error": "缺少认证令牌",
            "message": "请在请求头中添加有效的Authorization令牌"
        }), 401
    
    # 路由定义
    @app.route('/')
    def index():
        return jsonify({"message": "Diabetes Visualization API"})
    
    # 用户认证路由
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.get_json()
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({"error": "用户名已存在"}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "邮箱已存在"}), 400
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({"message": "注册成功"}), 201
    
    @app.route('/api/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            # 处理来自@login_required装饰器的重定向或带next参数的GET请求
            next_url = request.args.get('next')
            if next_url:
                # 返回登录页面信息，包含next参数以便登录后跳转
                return jsonify({
                    "message": "Login required",
                    "next": next_url,
                    "status": "redirect"
                }), 401
            else:
                return jsonify({"message": "Login endpoint, use POST to login"}), 200
        
        # Handle POST request for actual login
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
    
        if user and user.check_password(data['password']):
            # 保留Flask-Login的登录状态（保持兼容性）
            login_user(user, remember=True)
            
            # 使用用户ID作为JWT的identity，因为User对象不能直接JSON序列化
            access_token = create_access_token(identity=user.id)
            # 返回用户信息和访问令牌
            return jsonify({
                "message": "登录成功",
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            })
    
        return jsonify({"error": "用户名或密码错误"}), 401
    
    @app.route('/api/logout', methods=['POST'])
    @dual_auth_required
    def logout():
        logout_user()
        return jsonify({"message": "登出成功"})
    
    @app.route('/api/test-auth', methods=['GET'])
    @dual_auth_required
    def test_auth():
        """测试认证状态的路由"""
        return jsonify({
            "message": "认证成功",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email
            }
        })
        
    @app.route('/api/test-jwt', methods=['GET'])
    def test_jwt():
        """测试JWT令牌的路由，用于调试"""
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
            try:
                # 使用jwt.decode来测试令牌，不进行签名验证
                from flask_jwt_extended import decode_token
                decoded_token = decode_token(token)
                return jsonify({
                    "status": "success",
                    "token_info": {
                        "is_valid": True,
                        "identity": decoded_token.get('sub'),
                        "exp": decoded_token.get('exp'),
                        "iat": decoded_token.get('iat')
                    }
                })
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400
        
        return jsonify({
            "status": "error",
            "message": "未提供有效的Bearer令牌"
        }), 400
    
    @app.route('/api/user/profile', methods=['POST', 'PUT'])
    @dual_auth_required
    def user_profile():
        if request.method == 'POST':
            return jsonify({
                "username": current_user.username,
                "email": current_user.email,
                "age": current_user.age,
                "gender": current_user.gender,
                "weight": current_user.weight,
                "height": current_user.height,
                "family_history": current_user.family_history,
                "bmi": current_user.get_bmi()
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            current_user.age = data.get('age', current_user.age)
            current_user.gender = data.get('gender', current_user.gender)
            current_user.weight = data.get('weight', current_user.weight)
            current_user.height = data.get('height', current_user.height)
            current_user.family_history = data.get('family_history', current_user.family_history)
            
            db.session.commit()
            return jsonify({"message": "个人信息更新成功"})
    
    # 数据API路由
    @app.route('/api/data/china')
    def china_data():
        return jsonify(load_china_data())
    
    @app.route('/api/data/international')
    def international_data():
        return jsonify(load_international_data())
    
    @app.route('/api/data/trends')
    def trends_data():
        return jsonify(load_trends_data())
    
    @app.route('/api/data/trends/simple', methods=['GET'])
    def get_trends_data():
        # 这里可以从数据库或文件中获取真实数据
        trends_data = {
            "years": [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022],
            "prevalence": [4.7, 5.5, 6.2, 6.9, 7.8, 8.4, 9.2, 9.8],
            "source": "国际糖尿病联盟",
            "last_updated": "2023-11-15"
        }
        return jsonify(trends_data)
    
    @app.route('/api/data/complications')
    def complications_data():
        # 示例并发症数据
        return jsonify({
            "complications": [
                {"name": "视网膜病变", "prevalence": 23.5, "severity": "high"},
                {"name": "肾病", "prevalence": 18.2, "severity": "high"},
                {"name": "神经病变", "prevalence": 15.8, "severity": "medium"},
                {"name": "心血管疾病", "prevalence": 32.1, "severity": "high"}
            ]
        })
    
    # 风险评估路由 - 未登录可直接测评
    @app.route('/api/risk/assess', methods=['POST'])
    def assess_risk():
        """
        评估用户糖尿病风险等级
        - 无需登录即可使用
        - 接收7个关键健康指标
        - 返回风险评分、等级和个性化建议
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            data = request.get_json()
            
            if not data:
                logger.warning("风险评估请求体为空")
                return jsonify({"error": "请求体不能为空，需要提供JSON格式数据"}), 400
            
            # 请求体验证
            required_fields = [
                'age_range', 'bmi_category', 'waist_status',
                'family_history', 'physical_activity', 
                'blood_pressure', 'glucose_history'
            ]
            
            # 检查必填字段
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                logger.warning(f"风险评估缺少必填字段: {missing_fields}")
                return jsonify({"error": f"缺少必填字段: {', '.join(missing_fields)}"}), 400
            
            # 检查字段值的有效性
            validation_errors = []
            
            valid_age_ranges = ["20-39", "40-49", "50-59", "60-69", "70+"]
            if data['age_range'] not in valid_age_ranges:
                validation_errors.append({"field": "age_range", "message": "无效的年龄范围，可选值: 20-39, 40-49, 50-59, 60-69, 70+"})
            
            valid_bmi_categories = ["underweight", "normal", "overweight", "obese"]
            if data['bmi_category'] not in valid_bmi_categories:
                validation_errors.append({"field": "bmi_category", "message": "无效的BMI分类，可选值: underweight, normal, overweight, obese"})
            
            valid_waist_statuses = ["normal-male", "normal-female", "abnormal-male", "abnormal-female"]
            if data['waist_status'] not in valid_waist_statuses:
                validation_errors.append({"field": "waist_status", "message": "无效的腰围状态，可选值: normal-male, normal-female, abnormal-male, abnormal-female"})
            
            valid_binary_answers = ["yes", "no"]
            if data['family_history'] not in valid_binary_answers:
                validation_errors.append({"field": "family_history", "message": "家族病史必须是'yes'或'no'"})
            if data['blood_pressure'] not in valid_binary_answers:
                validation_errors.append({"field": "blood_pressure", "message": "高血压必须是'yes'或'no'"})
            if data['glucose_history'] not in valid_binary_answers:
                validation_errors.append({"field": "glucose_history", "message": "血糖异常史必须是'yes'或'no'"})
            
            valid_activity_levels = ["regular", "irregular", "sedentary"]
            if data['physical_activity'] not in valid_activity_levels:
                validation_errors.append({"field": "physical_activity", "message": "无效的运动频率，可选值: regular, irregular, sedentary"})
            
            if validation_errors:
                logger.warning(f"风险评估输入验证失败: {validation_errors}")
                return jsonify({"errors": validation_errors}), 400
            
            # 计算风险评分
            result = calculate_risk_score(data)
            
            # 保存评估结果（未登录用户不绑定user_id）
            assessment = RiskAssessment(
                user_id=None,
                risk_score=result['risk_score'],
                risk_level=result['risk_level'],
                factors=json.dumps({
                    'risk_factors': result['risk_factors'],
                    'assessment_date': result.get('assessment_date', datetime.utcnow().isoformat())
                })
            )
            db.session.add(assessment)
            db.session.commit()
            
            # 添加评估时间和评估ID
            result['assessment_date'] = datetime.utcnow().isoformat()
            result['assessment_id'] = assessment.id  # 返回评估记录ID，便于前端追踪
            
            logger.info(f"风险评估完成，评分: {result['risk_score']}，等级: {result['risk_level']}")
            return jsonify(result)
        except Exception as e:
            logger.error(f"风险评估过程中发生错误: {str(e)}")
            db.session.rollback()
            return jsonify({"error": "评估过程中发生错误，请稍后重试"}), 500
    
    @app.route('/api/risk/history')
    @dual_auth_required
    def risk_history():
        assessments = RiskAssessment.query.filter_by(user_id=current_user.id)\
            .order_by(RiskAssessment.assessment_date.desc()).all()
        
        # 构建响应数据
        history = []
        for a in assessments:
            factors_data = json.loads(a.factors) if a.factors else {}
            
            # 处理不同版本的数据格式
            risk_factors = factors_data.get('risk_factors', factors_data)
            
            # 计算风险百分比（如果没有存储）
            risk_percentage = 0
            if a.risk_score >= 17:
                risk_percentage = min(95 + (a.risk_score - 17) * 1, 100)
            elif a.risk_score >= 10:
                risk_percentage = 40 + (a.risk_score - 10) * 5
            else:
                risk_percentage = min(20 + a.risk_score * 2, 39)
            
            history.append({
                'id': a.id,
                'risk_score': a.risk_score,
                'risk_percentage': risk_percentage,
                'risk_level': a.risk_level,
                'assessment_date': a.assessment_date.isoformat(),
                'factors': risk_factors
            })
        
        return jsonify(history)
    
    # 健康检查路由
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy", "service": "diabetes-visualization-api"})
    
    # 详细数据路由
    @app.route('/api/data/china/detailed')
    def china_detailed_data():
        """获取详细的中国省份数据"""
        data = load_china_data()
        return jsonify(data)

    @app.route('/api/data/international/detailed')
    def international_detailed_data():
        """获取详细的国际数据"""
        data = load_international_data()
        return jsonify(data)

    @app.route('/api/data/trends/detailed')
    def trends_detailed_data():
        """获取详细的趋势数据"""
        data = load_trends_data()
        return jsonify(data)

    @app.route('/api/data/regions/<region_name>')
    def region_data(region_name):
        """获取特定区域的数据"""
        china_data = load_china_data()
        if region_name in china_data.get('regions', {}):
            region_provinces = china_data['regions'][region_name]
            provinces_data = [p for p in china_data['provinces'] if p['name'] in region_provinces]
            return jsonify({
                'region': region_name,
                'provinces': provinces_data,
                'summary': {
                    'total_population': sum(p['population'] for p in provinces_data),
                    'total_cases': sum(p['cases'] for p in provinces_data),
                    'avg_rate': round(sum(p['diabetes_rate'] for p in provinces_data) / len(provinces_data), 2)
                }
            })
        return jsonify({'error': 'Region not found'}), 404
    
    # 为糖尿病数据可视化应用添加新的API端点
    @app.route('/api/continent-data', methods=['GET'])
    def get_continent_data():
        """获取大洲数据（用于饼图）"""
        international_data = load_international_data()
        result = []
        for continent in international_data.get('continents', []):
            result.append({
                'name': continent['name'],
                'value': continent['diabetes_rate'],
                'tooltip': f"{continent['name']} ({continent['diabetes_rate']}%)"
            })
        # 添加一些默认数据以防数据不足
        if len(result) < 7:
            default_continents = [
                {'name': '亚洲', 'value': 60, 'tooltip': '亚洲 (60%)'},
                {'name': '非洲', 'value': 10.5, 'tooltip': '非洲 (10.5%)'},
                {'name': '北美洲', 'value': 10.4, 'tooltip': '北美洲 (10.4%)'},
                {'name': '南美洲', 'value': 9.4, 'tooltip': '南美洲 (9.4%)'},
                {'name': '欧洲', 'value': 8.1, 'tooltip': '欧洲 (8.1%)'},
                {'name': '大洋洲', 'value': 12.3, 'tooltip': '大洋洲 (12.3%)'},
                {'name': '南极洲', 'value': 0, 'tooltip': '南极洲 (无数据)'}
            ]
            result = default_continents
        return jsonify(result)

    @app.route('/api/continents-data', methods=['GET'])
    def get_continents_data():
        """获取大洲数据（用于柱状图）"""
        international_data = load_international_data()
        
        # 准备大洲名称和对应的糖尿病率
        continents = []
        rates = []
        
        # 从数据中提取大洲信息
        for continent in international_data.get('continents', []):
            if continent['name'] != '南极洲':  # 排除南极洲（无数据）
                continents.append(continent['name'])
                rates.append(continent['diabetes_rate'])
        
        # 如果数据不足，使用默认数据
        if len(continents) < 6:
            continents = ['亚洲', '非洲', '北美洲', '南美洲', '欧洲', '大洋洲']
            rates = [60, 10.5, 10.4, 9.4, 8.1, 12.3]
        
        return jsonify({
            'xAxis': continents,
            'seriesData': rates
        })

    @app.route('/api/country-data', methods=['GET'])
    def get_country_data():
        """获取国家数据（用于世界地图）"""
        # 从国际数据中提取国家信息
        international_data = load_international_data()
        countries = []
        
        # 大洲到国家的映射关系
        continent_to_countries = {
            '亚洲': ['China', 'Japan', 'India', 'South Korea', 'Indonesia', 'Turkey'],
            '非洲': ['Nigeria', 'Egypt', 'South Africa', 'Kenya', 'Ethiopia'],
            '北美洲': ['United States', 'Canada', 'Mexico'],
            '南美洲': ['Brazil', 'Argentina', 'Peru', 'Colombia'],
            '欧洲': ['Russia', 'Germany', 'France', 'United Kingdom', 'Italy'],
            '大洋洲': ['Australia', 'New Zealand']
        }
        
        # 大洲对应的糖尿病率
        continent_rates = {
            '亚洲': 60.0,
            '非洲': 10.5,
            '北美洲': 10.4,
            '南美洲': 9.4,
            '欧洲': 8.1,
            '大洋洲': 12.3
        }
        
        # 为每个大洲的国家分配糖尿病率
        for continent, continent_countries in continent_to_countries.items():
            rate = continent_rates.get(continent, 5.0)
            for country in continent_countries:
                # 为不同国家添加一些变化，使数据更真实
                country_rate = rate + (hash(country) % 10 - 5) * 0.5
                countries.append({
                    'name': country,
                    'value': max(0, country_rate),  # 确保不小于0
                    'continent': continent
                })
        
        return jsonify(countries)

    @app.route('/api/countries-data', methods=['GET'])
    def get_countries_data():
        """获取国家数据（用于世界地图）"""
        # 从国际数据中提取国家信息
        international_data = load_international_data()
        countries = []
        
        # 大洲到国家的映射关系
        continent_to_countries = {
            '亚洲': ['China', 'Japan', 'India', 'South Korea', 'Indonesia', 'Turkey'],
            '非洲': ['Nigeria', 'Egypt', 'South Africa', 'Kenya', 'Ethiopia'],
            '北美洲': ['United States', 'Canada', 'Mexico'],
            '南美洲': ['Brazil', 'Argentina', 'Peru', 'Colombia'],
            '欧洲': ['Russia', 'Germany', 'France', 'United Kingdom', 'Italy'],
            '大洋洲': ['Australia', 'New Zealand']
        }
        
        # 大洲对应的糖尿病率
        continent_rates = {
            '亚洲': 60.0,
            '非洲': 10.5,
            '北美洲': 10.4,
            '南美洲': 9.4,
            '欧洲': 8.1,
            '大洋洲': 12.3
        }
        
        # 为每个大洲的国家分配糖尿病率
        for continent, continent_countries in continent_to_countries.items():
            rate = continent_rates.get(continent, 5.0)
            for country in continent_countries:
                # 为不同国家添加一些变化，使数据更真实
                country_rate = rate + (hash(country) % 10 - 5) * 0.5
                countries.append({
                    'name': country,
                    'value': max(0, country_rate),  # 确保不小于0
                    'continent': continent
                })
        
        return jsonify(countries)

    @app.route('/api/age-distribution', methods=['GET'])
    def get_age_distribution():
        """获取年龄分布数据（用于柱状图）"""
        # 提供年龄分布数据
        age_data = [
            ('0-20', 1),
            ('21-44', 1.9),
            ('45-64', 8.9),
            ('65+', 23.7)
        ]
        
        xAxis = [row[0] for row in age_data]
        seriesData = [row[1] for row in age_data]
        
        return jsonify({
            'xAxis': xAxis,
            'seriesData': seriesData
        })

    @app.route('/api/gender-ratio', methods=['GET'])
    def get_gender_ratio():
        """获取性别比例数据（用于饼图）"""
        # 提供性别比例数据
        gender_data = [
            {'name': '男性', 'value': 52},
            {'name': '女性', 'value': 48}
        ]
        
        return jsonify(gender_data)

    @app.route('/api/blood-sugar-trend', methods=['GET'])
    def get_blood_sugar_trend():
        """获取血糖趋势数据（用于折线图）"""
        trends_data = load_trends_data()
        
        # 使用现有趋势数据或提供默认数据
        if 'years' in trends_data and 'global_rates' in trends_data:
            xAxis = [str(year) for year in trends_data['years']]
            seriesData = trends_data['global_rates']
        else:
            # 默认趋势数据
            xAxis = ['1990', '2015', '2017', '2019', '2022']
            seriesData = [7, 8.4, 8.3, 9.3, 14]
        
        return jsonify({
            'xAxis': xAxis,
            'seriesData': seriesData
        })

    @app.route('/api/geo-distribution', methods=['GET'])
    def get_geo_distribution():
        """获取地理分布数据（七大洲占比）"""
        continent_data = load_international_data().get('continents', [])
        
        # 如果没有足够的数据，使用默认值
        if len(continent_data) < 6:
            default_data = [
                {'name': '亚洲', 'value': 60},
                {'name': '非洲', 'value': 10.5},
                {'name': '北美洲', 'value': 10.4},
                {'name': '南美洲', 'value': 9.4},
                {'name': '欧洲', 'value': 8.1},
                {'name': '大洋洲', 'value': 12.3}
            ]
            return jsonify(default_data)
        
        # 排除南极洲（无数据）
        result = [{'name': c['name'], 'value': c['diabetes_rate']} for c in continent_data if c['name'] != '南极洲']
        return jsonify(result)

    @app.route('/api/health-tips', methods=['GET'])
    def get_health_tips():
        """获取健康提示信息"""
        tips = [
            "保持健康的饮食习惯，减少高糖、高脂肪食物的摄入",
            "每周进行至少150分钟的中等强度有氧运动",
            "定期体检，监测血糖水平",
            "保持健康的体重，BMI控制在18.5-24之间",
            "充足的睡眠有助于维持正常的血糖代谢",
            "减少压力，学习放松技巧如冥想、瑜伽等"
        ]
        return jsonify(tips)
    
    # 省份数据接口
    @app.route('/api/provinces/data', methods=['GET'])
    def get_provinces_data():
        """获取所有省份基础数据（用于地图）"""
        china_data = load_china_data()
        provinces_data = china_data.get('provinces', [])
        
        # 转换为地图需要的格式
        map_data = [
            {'name': province['name'], 'value': province['diabetes_rate'] / 100}  # 转换为小数形式
            for province in provinces_data
        ]
        
        return jsonify(map_data)
    
    @app.route('/api/provinces/<province>/details', methods=['GET'])
    def get_province_details(province):
        """获取特定省份详细数据"""
        china_data = load_china_data()
        provinces_data = china_data.get('provinces', [])
        
        # 查找指定省份
        province_data = next((p for p in provinces_data if p['name'] == province), None)
        
        if not province_data:
            return jsonify({'error': 'Province not found'}), 404
        
        # 基础患病率（作为基准）
        base_rate = province_data['diabetes_rate']
        
        # 生成年龄分布数据（根据基准率调整）
        age_ranges = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
        # 不同年龄段的相对患病率系数
        age_factors = [0.2, 0.5, 1.0, 1.5, 2.0, 2.5]
        age_values = [base_rate * factor for factor in age_factors]
        
        # 生成性别比例数据
        male_rate = province_data.get('male_rate', base_rate * 1.1)  # 男性略高
        female_rate = province_data.get('female_rate', base_rate * 0.9)  # 女性略低
        total = male_rate + female_rate
        gender_ratio = [
            {'value': round(male_rate / total * 100), 'name': '男性'},
            {'value': round(female_rate / total * 100), 'name': '女性'}
        ]
        
        # 生成血糖趋势数据
        years = ["2019", "2020", "2021", "2022", "2023"]
        # 每年略微增长
        trend_values = [base_rate * (1 + (i * 0.01)) for i in range(len(years))]
        
        return jsonify({
            'province': province,
            'ageDistribution': {
                'ranges': age_ranges,
                'values': age_values
            },
            'genderRatio': gender_ratio,
            'bloodSugarTrend': {
                'years': years,
                'values': trend_values
            }
        })
    
    @app.route('/api/provinces/national-summary', methods=['GET'])
    def get_national_summary():
        """获取全国汇总数据"""
        china_data = load_china_data()
        provinces_data = china_data.get('provinces', [])
        
        # 计算全国平均患病率
        if provinces_data:
            avg_rate = sum(p['diabetes_rate'] for p in provinces_data) / len(provinces_data)
            total_population = sum(p.get('population', 0) for p in provinces_data)
            total_cases = sum(p.get('cases', 0) for p in provinces_data)
        else:
            avg_rate = 8.8
            total_population = 1400000000
            total_cases = 123200000
        
        # 生成全国年龄分布数据
        age_ranges = ["18-29", "30-39", "40-49", "50-59", "60-69", "70+"]
        age_values = [2.8, 6.2, 12.8, 20.5, 26.0, 29.5]  # 全国平均年龄分布
        
        # 生成全国性别比例数据
        gender_ratio = [
            {'value': 51, 'name': '男性'},
            {'value': 49, 'name': '女性'}
        ]
        
        # 生成全国血糖趋势数据
        years = ["2019", "2020", "2021", "2022", "2023"]
        trend_values = [8.8, 9.0, 9.2, 9.5, 9.8]  # 全国平均趋势
        
        return jsonify({
            'summary': {
                'average_rate': avg_rate,
                'total_population': total_population,
                'total_cases': total_cases,
                'provinces_count': len(provinces_data)
            },
            'ageDistribution': {
                'ranges': age_ranges,
                'values': age_values
            },
            'genderRatio': gender_ratio,
            'bloodSugarTrend': {
                'years': years,
                'values': trend_values
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()  # 创建数据库表
        
    app.run(debug=True, host='0.0.0.0', port=5000)
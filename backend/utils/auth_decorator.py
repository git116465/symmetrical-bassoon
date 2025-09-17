from functools import wraps
from flask import request, jsonify, current_app, g
from flask_login import current_user
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import logging
from functools import wraps

# 配置日志记录
def setup_logger():
    logger = logging.getLogger('auth_decorator')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def dual_auth_required(fn):
    """
    自定义认证装饰器，同时支持Flask-Login和JWT认证
    - 首先尝试使用JWT令牌认证，如果请求头中包含Authorization: Bearer token
    - 否则尝试使用Flask-Login的session认证
    - JWT验证错误会由app.py中的错误处理器捕获并返回详细信息
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        logger = setup_logger()
        
        # 记录请求头和路径用于调试
        auth_header = request.headers.get('Authorization')
        logger.debug(f"请求路径: {request.path}")
        logger.debug(f"Authorization头存在: {auth_header is not None}")
        
        # 1. 如果有JWT令牌，使用JWT认证
        if auth_header and auth_header.startswith('Bearer '):
            logger.debug("检测到Bearer令牌，尝试JWT认证")
            try:
                # 验证JWT令牌
                verify_jwt_in_request()
                # 获取JWT中的用户身份
                jwt_identity = get_jwt_identity()
                jwt_data = get_jwt()
                
                logger.debug(f"JWT认证成功，用户ID: {jwt_identity}")
                logger.debug(f"JWT数据: {jwt_data}")
                
                if jwt_identity:
                    # JWT认证成功，继续处理请求
                    return fn(*args, **kwargs)
                else:
                    logger.error("JWT令牌中未包含有效的用户身份")
                    return jsonify({"error": "认证失败", "message": "JWT令牌中未包含有效的用户身份"}), 401
            except Exception as e:
                # 记录异常信息以进行调试
                logger.error(f"JWT认证失败: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                # 重新抛出异常，让JWT错误处理器处理
                raise
        
        # 2. 如果没有JWT令牌，尝试使用Flask-Login的session认证
        logger.debug(f"Flask-Login认证状态: {current_user.is_authenticated}")
        if current_user.is_authenticated:
            logger.debug(f"Flask-Login认证成功，用户: {current_user.username}")
            # Flask-Login认证成功，继续处理请求
            return fn(*args, **kwargs)
        
        # 3. 两种认证都失败，返回401错误
        logger.error("所有认证方式失败")
        return jsonify({"error": "认证失败，需要登录", "message": "请提供有效的认证信息"}), 401
    
    return decorated_function

def simple_auth_required(fn):
    """
    简化的认证装饰器，直接使用before_request中设置的g.user
    不再单独验证JWT，而是依赖全局的before_request处理
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return jsonify({"error": "认证失败", "message": "需要有效的JWT令牌"}), 401
        return fn(*args, **kwargs)
    
    return decorated_function
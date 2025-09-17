from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import json

# 初始化数据库实例
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    family_history = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系定义
    assessments = db.relationship('RiskAssessment', backref='user', lazy=True)
    
    def set_password(self, password):
        """设置用户密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """检查用户密码是否正确"""
        return check_password_hash(self.password_hash, password)
    
    def get_bmi(self):
        """计算BMI指数"""
        if self.weight and self.height and self.height > 0:
            return round(self.weight / ((self.height / 100) ** 2), 1)
        return None
    
    def to_dict(self):
        """将用户对象转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age,
            'gender': self.gender,
            'weight': self.weight,
            'height': self.height,
            'family_history': self.family_history,
            'bmi': self.get_bmi(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class RiskAssessment(db.Model):
    """风险评估模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_score = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)
    factors = db.Column(db.Text)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """将风险评估对象转换为字典格式"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'risk_score': self.risk_score,
            'risk_level': self.risk_level,
            'factors': json.loads(self.factors) if self.factors else {},
            'assessment_date': self.assessment_date.isoformat()
        }
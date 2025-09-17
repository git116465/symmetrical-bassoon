import requests
import json

# 测试认证流程
def test_authentication():
    base_url = "http://localhost:5000"
    
    # 创建一个会话对象来保持Cookie
    session = requests.Session()
    session.headers.update({'Content-Type': 'application/json'})
    
    # 测试登录
    login_data = {
        "username": "testuser",  # 替换为实际存在的用户名
        "password": "testpassword"  # 替换为实际密码
    }
    
    print("正在登录...")
    login_response = session.post(f"{base_url}/api/login", data=json.dumps(login_data))
    print(f"登录响应: {login_response.status_code}")
    print(f"登录内容: {login_response.json()}")
    
    # 如果登录成功，测试受保护的路由
    if login_response.status_code == 200:
        print("\n测试访问受保护的路由...")
        
        # 测试个人资料路由
        profile_response = session.post(f"{base_url}/api/user/profile")
        print(f"个人资料响应: {profile_response.status_code}")
        print(f"个人资料内容: {profile_response.json()}")
        
        # 测试风险评估路由
        risk_data = {
            "age_range": "40-49",
            "bmi_category": "normal",
            "waist_status": "normal-male",
            "family_history": "no",
            "physical_activity": "regular",
            "blood_pressure": "no",
            "glucose_history": "no"
        }
        risk_response = session.post(f"{base_url}/api/risk/assess", data=json.dumps(risk_data))
        print(f"风险评估响应: {risk_response.status_code}")
        print(f"风险评估内容: {risk_response.json()}")
    
if __name__ == "__main__":
    test_authentication()
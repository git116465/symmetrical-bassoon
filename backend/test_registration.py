import requests
import json

# 定义API基础URL
BASE_URL = 'http://localhost:5000/api'

# 测试注册功能
def test_registration():
    # 测试用户数据
    test_user = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    print("测试注册功能...")
    response = requests.post(f"{BASE_URL}/register", json=test_user)
    
    print(f"注册响应状态码: {response.status_code}")
    print(f"注册响应内容: {response.json()}")
    
    # 如果注册成功，测试登录
    if response.status_code == 201:
        print("\n测试登录功能...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        login_response = requests.post(f"{BASE_URL}/login", json=login_data)
        
        print(f"登录响应状态码: {login_response.status_code}")
        print(f"登录响应内容: {login_response.json()}")
        
        # 如果登录成功，测试认证状态
        if login_response.status_code == 200:
            # 获取登录后的cookie
            cookies = login_response.cookies
            
            print("\n测试认证状态...")
            auth_response = requests.get(f"{BASE_URL}/test-auth", cookies=cookies)
            
            print(f"认证响应状态码: {auth_response.status_code}")
            print(f"认证响应内容: {auth_response.json()}")

if __name__ == "__main__":
    print("开始测试用户注册登录功能...")
    test_registration()
    print("测试完成")
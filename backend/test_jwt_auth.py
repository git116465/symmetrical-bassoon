import requests
import json

# 测试配置
BASE_URL = 'http://localhost:5000'
TEST_USERNAME = 'testuser'
TEST_PASSWORD = 'testpassword'
TEST_EMAIL = 'test@example.com'

# 清理之前的测试用户
print("清理之前的测试用户...")
response = requests.post(f"{BASE_URL}/api/login", json={
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD
})
if response.status_code == 200:
    token = response.json()['access_token']
    requests.post(f"{BASE_URL}/api/logout", headers={
        "Authorization": f"Bearer {token}"
    })

# 1. 测试用户注册
print("\n1. 测试用户注册...")
register_response = requests.post(f"{BASE_URL}/api/register", json={
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD,
    "email": TEST_EMAIL
})
print(f"注册响应状态码: {register_response.status_code}")
print(f"注册响应内容: {register_response.json()}")

# 2. 测试用户登录并获取JWT令牌
print("\n2. 测试用户登录并获取JWT令牌...")
login_response = requests.post(f"{BASE_URL}/api/login", json={
    "username": TEST_USERNAME,
    "password": TEST_PASSWORD
})
print(f"登录响应状态码: {login_response.status_code}")

if login_response.status_code == 200:
    login_data = login_response.json()
    print(f"登录响应内容: {login_data}")
    access_token = login_data.get('access_token')
    
    # 3. 使用JWT令牌访问受保护资源
    print("\n3. 使用JWT令牌访问受保护资源...")
    auth_headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # 测试/test-auth路由
    test_auth_response = requests.get(f"{BASE_URL}/api/test-auth", headers=auth_headers)
    print(f"/api/test-auth响应状态码: {test_auth_response.status_code}")
    print(f"/api/test-auth响应内容: {test_auth_response.json()}")
    
    # 测试/user/profile路由
    profile_response = requests.post(f"{BASE_URL}/api/user/profile", headers=auth_headers)
    print(f"/api/user/profile响应状态码: {profile_response.status_code}")
    print(f"/api/user/profile响应内容: {profile_response.json()}")
    
    # 4. 测试未授权访问
    print("\n4. 测试未授权访问...")
    no_auth_response = requests.get(f"{BASE_URL}/api/test-auth")
    print(f"未授权访问状态码: {no_auth_response.status_code}")
    print(f"未授权访问响应内容: {no_auth_response.json()}")
    
    # 5. 测试JWT令牌过期处理（可选，需要修改JWT配置）
    # print("\n5. 测试JWT令牌过期处理...")
    # 这里需要等待令牌过期，或者修改JWT配置使过期时间很短
    
    # 6. 测试用户登出
    print("\n6. 测试用户登出...")
    logout_response = requests.post(f"{BASE_URL}/api/logout", headers=auth_headers)
    print(f"登出响应状态码: {logout_response.status_code}")
    print(f"登出响应内容: {logout_response.json()}")
    
    # 7. 测试登出后访问受保护资源
    print("\n7. 测试登出后访问受保护资源...")
    after_logout_response = requests.get(f"{BASE_URL}/api/test-auth", headers=auth_headers)
    print(f"登出后访问状态码: {after_logout_response.status_code}")
    print(f"登出后访问响应内容: {after_logout_response.json()}")
else:
    print("登录失败，无法继续测试")

print("\n测试完成！")
import requests


########################################################3
# 1. 定義 API 網址
url = "https://webhook.site/6638131a-3c93-4ed9-b22d-07fe02e76067/post"

# 2. 發出請求
response = requests.post(url)

data = {
    "user": "test_user",
    "job": "QA_Engineer"
}

response = requests.post(url, data=data)

print(response)

print(f"狀態碼: {response.status_code}")
print(f"回應標頭: {response.headers.get('Content-Encoding')}") 
print(f"內容類型: {response.headers.get('Content-Type')}")
# print(response_header.text)


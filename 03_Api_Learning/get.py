import requests

# 1. 定義 API 網址
url = "https://httpbin.org/get"

# 2. 發出請求
response = requests.get(url)

print(response.status_code)
print(response.headers)
print(response.text)



# 1. 定義 API 網址
url_brotli = "https://httpbin.org/brotli"

# 2. 發出請求
response_brotli = requests.get(url_brotli)

print(f"狀態碼: {response_brotli.status_code}")
print(f"回應標頭: {response_brotli.headers.get('Content-Encoding')}") # 應該會顯示 'br'
print(f"內容類型: {response_brotli.headers.get('Content-Type')}")
print(response_brotli.text)

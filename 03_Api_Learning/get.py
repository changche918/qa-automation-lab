import requests

# 1. 定義 API 網址
url = "https://httpbin.org/get"

# 2. 發出請求
response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應標頭: {response.headers.get('Content-Encoding')}") 
print(f"內容類型: {response.headers.get('Content-Type')}")
print(response.text)

# # ==================================================

# # 1. 定義 API 網址
# url_brotli = "https://httpbin.org/brotli"

# # 2. 發出請求
# response_brotli = requests.get(url_brotli)

# print(f"狀態碼: {response_brotli.status_code}")
# print(f"回應標頭: {response_brotli.headers.get('Content-Encoding')}") # 應該會顯示 'br'
# print(f"內容類型: {response_brotli.headers.get('Content-Type')}")
# print(response_brotli.text)

# # ==================================================

# 1. 定義 API 網址
url_header = "https://httpbin.org/headers"

# 2. 發出請求
response_header = requests.get(url_header)

print(f"狀態碼: {response_header.status_code}")
print(f"回應標頭: {response_header.headers.get('Content-Encoding')}") 
print(f"內容類型: {response_header.headers.get('Content-Type')}")
print(response_header.text)

# ==================================================

# # 巴哈
# # 1. 定義 API 網址
# url_gamer = "https://api.gamer.com.tw/lite/v1/get_jid.php?bsn=23805"

# # 2. 發出請求
# response_gamer = requests.get(url_gamer)

# print(f"狀態碼: {response_gamer.status_code}")
# print(f"回應標頭: {response_gamer.headers.get('Content-Encoding')}") 
# print(f"內容類型: {response_gamer.headers.get('Content-Type')}")
# print(response_gamer.text)



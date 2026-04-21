import requests

# ============================================================
#  Redirects（重新導向）
# ============================================================
# 3xx 狀態碼代表「東西在別的地方」，requests 預設會自動跟著跳。
#
# 常見：
#   301 永久搬家
#   302 暫時搬家
#   307/308 跳轉且保留原本的 HTTP 方法
#
# 跳轉次數上限預設 30 次，超過會拋 TooManyRedirects

# ============================================================
# --- 自動跟著跳轉（預設行為）---
# ============================================================
# /absolute-redirect/10 會連續跳轉 10 次才到終點
url = "https://httpbin.org/absolute-redirect/10"

# allow_redirects 預設 True，requests 會自動跟完所有跳轉
response = requests.get(
    url,
    timeout=5
)

print(f"狀態碼: {response.status_code}")
print(f"經過了幾次跳轉: {len(response.history)}") 
"""
hitory 是一個 list，裡面是每次跳轉的 response 物件
裡面有 status,headers,url,text
"""
for row in response.history: # 20260420 用自己方式解釋物件(for迴圈)，相似的情境 ?
    print(f"{row.status_code} → {row.headers.get('Location')}")  # 每次跳轉的狀態碼 + 下一個 URL

row status 200 herders , 
row status 200 herders ,

print(f"回應內容: {response.text}")
# 20260420 get vs ['Location'] 差異 ? 優缺點
# 為什麼可以這樣寫 ["Location"] 20260420
# ============================================================
# 進階用法
# ============================================================
# 不自動跳轉，只看第一層：
# response = requests.get(url, allow_redirects=False)
print(response.status_code, response.headers["Location"])  # 302 + 下一個 URL # 20260420 為什麼可以這樣寫 ["Location"]
data[0,1,2,3]

# 限制跳轉次數：
# session = requests.Session()
# session.max_redirects = 5
#
# 查看完整跳轉路徑：
# for r in response.history:
#     print(f"  {r.status_code} → {r.headers.get( 'Location')}")

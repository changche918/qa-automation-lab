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
# --- 備註 ---
# requests 會把所有跳轉自動跟完，最後給你的 response 就是 /get 那個 200。
# 然後中間 10 次跳轉全部存在 response.history 裡
for row in response.history: # 20260420 用自己方式解釋物件(for迴圈)，相似的情境 ?
    print(f"{row.status_code} → {row.headers.get('Location')}")  # 每次跳轉的狀態碼 + 下一個 URL

print(f"回應內容: {response.text}")

# 20260420 get vs ['Location'] 差異 ? 優缺點


# ============================================================
# 進階用法
# ============================================================

response = requests.get(url, allow_redirects=False)
print(response.status_code, response.headers["Location"])  # 302 + 下一個 URL 

""" 
1. ["Location"]，他不分大小寫 Location 也可，他是 requests 套件的功能，是字典
2. 用 [] 取值的情境 :
    # 1. list（用整數當「位置」index）
    nums = [10, 20, 30]
    nums[0]              # 10  ← 第 0 個元素

    # 2. dict（用 key 當「鑰匙」）
    user = {"name": "Ryan", "age": 30}
    user["name"]         # "Ryan"  ← 用 key 取對應的 value

    # 3. 字串（用整數 index 取單個字元）
    text = "hello"
    text[0]              # "h"

    # 4. tuple
    point = (10, 20)
    point[1]             # 20
"""


# 限制跳轉次數：
# session = requests.Session()
# session.max_redirects = 5
#
# 查看完整跳轉路徑：
# for r in response.history:
#     print(f"  {r.status_code} → {r.headers.get( 'Location')}")

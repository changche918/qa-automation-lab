import requests

# # 1. 定義 API 網址
# url = "https://httpbin.org/get"

# # 2. 發出請求
# response = requests.get(url)

# print(f"狀態碼: {response.status_code}")
# print(f"回應標頭: {response.headers.get('Content-Encoding')}") 
# print(f"內容類型: {response.headers.get('Content-Type')}")
# print(response.text)

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

# # 1. 定義 API 網址
# url_header = "https://httpbin.org/headers"

# # 2. 發出請求
# response_header = requests.get(url_header)

# print(f"狀態碼: {response_header.status_code}")
# print(f"回應標頭: {response_header.headers.get('Content-Encoding')}") 
# print(f"內容類型: {response_header.headers.get('Content-Type')}")
# print(response_header.text)

# ==================================================

# 巴哈神魔版，自己帶 header，模擬瀏覽器行為
# url_gamer = "https://api.gamer.com.tw/lite/v1/get_jid.php?bsn=23805"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
#     "Referer": "https://www.gamer.com.tw/",
#     "Origin": "https://www.gamer.com.tw",
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
# }

# response_gamer = requests.get(url_gamer, headers=headers)

# print(f"狀態碼: {response_gamer.status_code}")
# print(response_gamer.text)


# ===== AI 提供 =====
from bs4 import BeautifulSoup

url = "https://forum.gamer.com.tw/B.php?bsn=23805"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://forum.gamer.com.tw/",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = []
links = soup.find_all("a")

for link in links:
    text = link.get_text(strip=True)
    href = link.get("href", "")
    
    # 只要有 snA 參數的（文章主連結），排除純數字（頁碼）和日期格式
    if "C.php" in href and "snA" in href and "page" not in href and "last" not in href:
        if text and not text.isdigit():
            articles.append({
                "title": text,
                "url": "https://forum.gamer.com.tw/" + href
            })

for i, a in enumerate(articles, 1):
    print(f"{i}. {a['title']}")
    print(f"   {a['url']}")
    print()
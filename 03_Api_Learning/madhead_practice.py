import requests

# 巴哈神魔版，自己帶 header，模擬瀏覽器行為
# url_gamer = "https://forum.gamer.com.tw/B.php?bsn=23805"
url_gamer_content = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=730010&tnum=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    # "Referer": "https://www.gamer.com.tw/",
    # "Origin": "https://www.gamer.com.tw",
    # "Accept": "application/json, text/plain, */*",
    # "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

# response_gamer = requests.get(url_gamer, headers=headers)
response_gamer_content = requests.get(url_gamer_content, headers=headers)

print(f"狀態碼: {response_gamer_content.status_code}")
print(response_gamer_content.text)
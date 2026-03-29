import requests

# 1. 定義 API 網址 (Endpoint)
url = "https://jsonplaceholder.typicode.com/posts/1"

# 2. 發出請求
response = requests.get(url)

# 3. 檢查狀態碼 (200 代表成功)
if response.status_code == 200:
    # 4. 將回傳的 JSON 轉為 Python 字典 (Dictionary)
    data = response.json()
    print(f"成功抓取！文章標題是：{data['title']}")
else:
    print(f"請求失敗，狀態碼：{response.status_code}")
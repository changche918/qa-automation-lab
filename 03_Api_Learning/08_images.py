import requests

# ============================================================
#  Images
# ============================================================

# --- GET ---
url = "https://httpbin.org/image"

response = requests.get(url, headers={"Accept": "image/png"})
print(response)

print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")

# 將圖片存成檔案
with open("image.png", "wb") as f:
    f.write(response.content)

print("圖片已儲存為 image.png")
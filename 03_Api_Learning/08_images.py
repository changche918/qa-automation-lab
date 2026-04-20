import requests

# ============================================================
#  Images（圖片下載）
# ============================================================
# 回應不只有 JSON，還可能是圖片 / PDF / ZIP 這類二進位檔。
# 讀取方式差在一個字：
#   文字（HTML/JSON/純文字） → response.text / response.json()
#   二進位（圖片、檔案）     → response.content  (bytes)

# ============================================================
# --- 請求圖片並儲存到本機 ---
# ============================================================
# Accept: image/png 告訴伺服器要 PNG 格式；不指定 httpbin 可能回 webp
url = "https://httpbin.org/image"

response = requests.get(
    url, 
    headers={"Accept": "image/png"},
    timeout=5
)

print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")

# 存檔：
# - "wb" = write binary（用 "w" 存圖片會損毀）
# - response.content 是原始 bytes，不做任何解碼
with open("image.png", "wb") as f:
    f.write(response.content)

# ============================================================
# 進階：下載大型檔案用串流（streaming）
# ============================================================
# 大檔案一次 .content 全讀會爆記憶體，改用 stream=True 分塊讀取：
#
# with requests.get(url, stream=True) as r:
#     r.raise_for_status()
#     with open("large_file.zip", "wb") as f:
#         for chunk in r.iter_content(chunk_size=8192):  # 每次讀 8KB
#             f.write(chunk)

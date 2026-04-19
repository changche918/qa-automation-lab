import requests

# ============================================================
#  Images（圖片下載）
# ============================================================
# API 不只能回傳 JSON，也能回傳二進位檔案，例如圖片、PDF、ZIP 等。
# 關鍵差異：
#   文字資料  → 用 response.text 或 response.json() 讀取
#   二進位檔  → 必須用 response.content 讀取（bytes 格式），再寫入檔案

# ============================================================
# --- 請求圖片並儲存到本機 ---
# ============================================================

# 透過 Accept header 告訴伺服器「我想要 PNG 格式的圖片」
# 如果不指定，httpbin 預設可能回傳其他格式（如 webp）
# 常見圖片類型：image/png、image/jpeg、image/gif、image/webp
url = "https://httpbin.org/image"

response = requests.get(url, headers={"Accept": "image/png"})
print(response)  # 印出 Response 物件，確認連線正常

print(f"狀態碼: {response.status_code}")
print(f"內容類型: {response.headers.get('Content-Type')}")  # 應該是 image/png

# 儲存圖片：
# 1. 用 "wb" 模式開檔（write binary 寫入二進位）
#    → 若用 "w" 模式（純文字）儲存圖片，檔案會損毀
# 2. 用 response.content 取得原始 bytes
#    → response.content 不做任何解碼，原汁原味保留二進位資料
# 3. with 語法確保檔案寫完後自動關閉，即使中途出錯也不會讓檔案鎖住
with open("image.png", "wb") as f:
    f.write(response.content)

print("圖片已儲存為 image.png")

# ============================================================
# 進階：下載大型檔案時用串流（streaming）
# ============================================================
# 問題：大檔案若一次 response.content 全部讀進記憶體，會佔用大量 RAM。
# 解法：用 stream=True 讓 requests 不立即下載 body，改為分塊讀取。
#
# with requests.get(url, stream=True) as r:
#     r.raise_for_status()
#     with open("large_file.zip", "wb") as f:
#         for chunk in r.iter_content(chunk_size=8192):  # 每次讀 8KB
#             f.write(chunk)
#
# 這樣不論檔案多大，記憶體使用量都只有一個 chunk 的大小（8KB）。

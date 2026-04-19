import requests

# ============================================================
#  Dynamic Data（動態資料）
# ============================================================
# 這個章節示範兩個實用技巧：
#   1. Base64 解碼（接收伺服器用 Base64 編碼的資料）
#   2. Timeout（避免程式因 API 太慢而無限等待）

# ============================================================
# --- Base64 解碼 ---
# ============================================================
# Base64 是一種「把任意二進位資料轉成純文字」的編碼方式。
# 常見用途：
#   - 在 URL 或 JSON（只能放文字）裡傳輸圖片、二進位資料
#   - Basic Auth 的帳密就是用 Base64 編碼後放進 header
#   - 注意：Base64 只是編碼，不是加密，任何人都能輕易解碼
#
# 這個 URL 裡的 "SFRUUEJJTiBpcyBhd2Vzb21l" 就是 "HTTPBIN is awesome" 的 Base64 編碼。
# httpbin 伺服器會幫你解碼，直接回傳原始文字。
url = "https://httpbin.org/base64/SFRUUEJJTiBpcyBhd2Vzb21l"

response = requests.get(url)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.text}")  # 應該看到 "HTTPBIN is awesome"

# 若你自己要在 Python 中做 Base64 編解碼：
# import base64
# encoded = base64.b64encode(b"HTTPBIN is awesome").decode()  # 編碼
# decoded = base64.b64decode("SFRUUEJJTiBpcyBhd2Vzb21l").decode()  # 解碼

# ============================================================
# --- Timeout（請求逾時設定）---
# ============================================================
# 問題：如果 API 伺服器很慢或無回應，requests 預設會「永遠等待」，
#       導致你的程式卡住，什麼事都做不了。
# 解法：加上 timeout 參數，超過指定秒數就放棄並拋出 requests.exceptions.Timeout 例外。
#
# 這個 URL 故意設計成「等 10 秒才回應」。
url = "https://httpbin.org/delay/10"  # 打一個會慢 10 秒的 API，但我最多願意等 15 秒

# timeout=15 → 最多等 15 秒，夠用就能拿到回應，不夠就拋出 Timeout 例外
# timeout 可以是單一數字（整體超時）或 tuple（連線超時, 讀取超時）：
#   timeout=(3, 15)  → 連線最多等 3 秒，資料讀取最多等 15 秒
response = requests.get(url, timeout=15)

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.text}")

# ============================================================
# 實務上應該加上例外處理：
# ============================================================
# try:
#     response = requests.get(url, timeout=15)
#     response.raise_for_status()  # 若狀態碼是 4xx/5xx，自動拋出例外
#     print(response.json())
# except requests.exceptions.Timeout:
#     print("請求逾時，請稍後再試")
# except requests.exceptions.HTTPError as e:
#     print(f"HTTP 錯誤: {e}")
# except requests.exceptions.RequestException as e:
#     print(f"其他錯誤: {e}")

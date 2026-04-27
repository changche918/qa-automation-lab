import requests

# ============================================================
#  Response Formats（回應格式）
# ============================================================
# 伺服器用 Content-Type header 告訴你回應是什麼格式，
# 根據格式選對應的讀取方式：
#   .json()   → JSON
#   .text     → HTML / 純文字
#   .content  → 圖片、檔案等二進位 bytes

# ============================================================
# --- JSON（現代 API 最常見）---
# ============================================================
json_url = "https://httpbin.org/json"

json_response = requests.get(
    json_url,
    timeout=5
)

print(json_response.headers)  # 觀察所有 header
print(f"Content-Type: {json_response.headers.get('Content-Type')}")
print(f"Content-Type: {json_response.headers.get('Date')}")
print(f"解析後: {json_response.json()}")




# ============================================================
# --- HTML / 純文字 ---
# ============================================================
"""
html_url = "https://httpbin.org/html"

html_response = requests.get(
    html_url,
    timeout=5
)

print(f"Content-Type: {html_response.headers.get('Content-Type')}")
print(f"前 200 字:\n{html_response.text[:200]}")

# ============================================================
# --- 圖片 / 二進位檔 ---
# ============================================================
# 圖片這類二進位檔一定要用 .content（bytes），用 .text 會亂碼
image_url = "https://httpbin.org/image/png"

image_response = requests.get(
    image_url,
    timeout=5
)

print(f"Content-Type: {image_response.headers.get('Content-Type')}")
print(f"檔案大小: {len(image_response.content)} bytes")

with open("test.png", "wb") as f:   # "wb" = write binary
    f.write(image_response.content)

# ============================================================
# --- 根據 Content-Type 自動選讀取方式 ---
# ============================================================
# 不確定伺服器會回什麼格式時，先看 Content-Type 再決定怎麼讀
sample_response = requests.get("https://httpbin.org/json", timeout=5)
content_type = sample_response.headers.get("Content-Type", "")

if "json" in content_type:
    data = sample_response.json()
elif content_type.startswith("text/"):
    data = sample_response.text
else:
    data = sample_response.content

print(f"Content-Type: {content_type}")
print(f"讀取結果: {data}")

# ============================================================
# --- Brotli 壓縮（進階）---
# ============================================================
# 「壓縮編碼」(Content-Encoding) 和「資料格式」(Content-Type) 是兩件事。
# Brotli 壓縮率比 gzip 高，需 pip install brotli 才能讓 requests 自動解壓縮。

brotli_url = "https://httpbin.org/brotli"

brotli_response = requests.get(
    brotli_url,
    headers={"Accept-Encoding": "br"},
    timeout=5
)

print(f"Content-Encoding: {brotli_response.headers.get('Content-Encoding')}")
print(f"解壓後內容: {brotli_response.json()}")

"""
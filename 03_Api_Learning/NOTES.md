# API 學習筆記（QA 自動化測試工程師視角）

## 目錄
1. [什麼是 API](#什麼是-api)
2. [HTTP Methods（方法）](#http-methods方法)
3. [HTTP Status Code（狀態碼）](#http-status-code狀態碼)
4. [Request 結構](#request-結構)
5. [Response 結構](#response-結構)
6. [Content-Type 常見類型](#content-type-常見類型)
7. [Authentication（身分驗證）](#authentication身分驗證)
8. [RESTful API 設計觀念](#restful-api-設計觀念)
9. [QA 測試重點](#qa-測試重點)
10. [Python `requests` 實作範例](#python-requests-實作範例)
11. [業界常用工具](#業界常用工具)
12. [常見問題排查](#常見問題排查)

---

## 什麼是 API

**API（Application Programming Interface）** = 程式之間「對話的協議」。

- **前端 → 後端**：使用者點按鈕 → 前端打 API 給後端 → 後端查資料庫 → 回傳給前端顯示
- **服務 → 服務**：訂單系統打 API 給金流系統處理付款
- **手機 App → 雲端**：IG 開 App → 打 API 取得最新貼文

> QA 測試 API = 模擬「呼叫者」對「伺服器」打請求，驗證回應是否正確。

---

## HTTP Methods（方法）

| 方法 | 意義 | 用途範例 | 冪等性 (Idempotent) | 安全性 (Safe) |
|:---|:---|:---|:---:|:---:|
| **GET** | 讀取 | 獲取文章、搜尋商品 | ✅ | ✅ |
| **POST** | 新增 | 註冊帳號、發布貼文 | ❌ | ❌ |
| **PUT** | 取代 | 更新整份個人檔案（漏傳欄位會被清空） | ✅ | ❌ |
| **PATCH** | 修改 | 只更新部分欄位（如改密碼） | ❌（看實作） | ❌ |
| **DELETE** | 刪除 | 刪訂單、註銷帳號 | ✅ | ❌ |
| **HEAD** | 同 GET 但只回 header | 檢查資源是否存在、確認檔案大小 | ✅ | ✅ |
| **OPTIONS** | 詢問支援的方法 | CORS 預檢請求 | ✅ | ✅ |

### 冪等性 (Idempotent) — QA 必懂

> **冪等 = 同一個請求做 1 次 vs 100 次，結果一樣**

| 方法 | 冪等？ | 為什麼 |
|------|------|------|
| GET | ✅ | 讀 100 次資料還是同樣那筆 |
| PUT | ✅ | 把使用者改成 `name=Ryan`，做 100 次最後還是 `name=Ryan` |
| DELETE | ✅ | 刪一筆訂單 100 次，第一次刪掉，後面 99 次都是「找不到」 |
| POST | ❌ | 新增 100 次 = 多 100 筆資料 |
| PATCH | ❌ | `quantity += 1` 做 100 次，數量會變成 +100 |

**為什麼 QA 要在意？**
- 重試邏輯測試：網路斷掉重試，POST 可能會重複下單，要驗證有沒有「冪等性 token」防呆
- 回滾測試：DELETE 同一筆兩次，第二次該回 404 不該回 500

### 安全性 (Safe) — 不會改變伺服器狀態

GET / HEAD / OPTIONS 是 safe，**只讀不寫**。其他都會改變狀態。

---

## HTTP Status Code（狀態碼）

QA 工程師**最常碰**的就是狀態碼，分五大類：

### 2xx 成功
| 碼 | 名稱 | 用法 |
|----|------|------|
| **200** | OK | 一般成功（GET / PUT / PATCH / DELETE） |
| **201** | Created | 資源建立成功（POST 新增使用者） |
| **204** | No Content | 成功但沒有回應內容（DELETE 完通常用這個） |

### 3xx 重新導向
| 碼 | 名稱 | 用法 |
|----|------|------|
| **301** | Moved Permanently | 永久搬家（網址永遠改了） |
| **302** | Found | 暫時搬家（登入後跳轉） |
| **304** | Not Modified | 快取沒變，用本地版本 |

### 4xx 客戶端錯誤（呼叫方寫錯）
| 碼 | 名稱 | 用法 |
|----|------|------|
| **400** | Bad Request | 參數格式錯（少欄位、JSON 格式壞） |
| **401** | Unauthorized | **沒帶身分**或 token 失效（要登入） |
| **403** | Forbidden | **有身分但沒權限**（一般使用者打 admin API） |
| **404** | Not Found | 找不到資源 |
| **405** | Method Not Allowed | 用了不支援的 method（GET 該用 POST） |
| **409** | Conflict | 衝突（重複註冊同一個 email） |
| **422** | Unprocessable Entity | 格式對但內容無效（年齡填 -5） |
| **429** | Too Many Requests | 短時間打太多次（被限流 rate limit） |

### 5xx 伺服器錯誤
| 碼 | 名稱 | 用法 |
|----|------|------|
| **500** | Internal Server Error | 後端炸了（不該 catch 的例外） |
| **502** | Bad Gateway | 上游服務炸了 |
| **503** | Service Unavailable | 服務暫時不可用（維護中） |
| **504** | Gateway Timeout | 上游服務逾時 |

### QA 重點：401 vs 403 一定要分清楚

| 場景 | 該回什麼 |
|------|---------|
| 沒帶 Authorization header | **401** |
| Token 過期 | **401** |
| Token 有效但身分是 user，去打 admin API | **403** |
| 普通會員想看別人的訂單 | **403** |

---

## Request 結構

一個完整的 HTTP 請求由四個部分組成：

```
POST  /api/users  HTTP/1.1                         ← 1. Method + URL
Host: api.example.com                              ← 2. Headers
Content-Type: application/json
Authorization: Bearer eyJhbGci...

{                                                  ← 3. Body
  "name": "Ryan",
  "email": "ryan@example.com"
}
```

### 1. URL 結構（網址三種傳參方式）

```
https://api.example.com/users/123?fields=name,email
└─ scheme └─ host        └─ path  └─ query string
```

| 類型 | 範例 | 用途 |
|------|------|------|
| **Path Parameter** | `/users/123` | 識別「特定資源」（哪個使用者） |
| **Query Parameter** | `?page=2&size=20` | 過濾、分頁、排序 |
| **Body** | `{"name": "Ryan"}` | 新增/修改的資料內容 |

### 2. Headers（標頭）

| 常見 Header | 用途 |
|------------|------|
| `Content-Type` | 告訴伺服器 Body 是什麼格式（JSON、表單） |
| `Accept` | 告訴伺服器我希望收到什麼格式 |
| `Authorization` | 帶身分認證資訊（token、API key） |
| `User-Agent` | 表明客戶端身分（瀏覽器、App、爬蟲） |
| `Cookie` | 帶 session 給後端認 |
| `X-Request-ID` | 自訂的追蹤 ID（除錯/log 用） |

### 3. Body（請求主體）

只有 POST/PUT/PATCH 通常會帶 body，GET/DELETE 大多不帶。

---

## Response 結構

```
HTTP/1.1 201 Created                               ← 1. 狀態行
Content-Type: application/json                     ← 2. Headers
Date: Fri, 25 Apr 2026 10:00:00 GMT
X-Request-ID: abc123

{                                                  ← 3. Body
  "id": 123,
  "name": "Ryan",
  "email": "ryan@example.com",
  "created_at": "2026-04-25T10:00:00Z"
}
```

QA 驗證時要檢查：
- ✅ Status code 是不是 201
- ✅ Response body 結構正確（有 id、name、email）
- ✅ Headers 有沒有需要的（X-Request-ID、Content-Type）

---

## Content-Type 常見類型

| Content-Type | 用途 | Body 範例 |
|------------|------|-----------|
| `application/json` | **最常見**，REST API 標準 | `{"name": "Ryan"}` |
| `application/x-www-form-urlencoded` | 傳統 HTML 表單送出 | `name=Ryan&age=18` |
| `multipart/form-data` | 上傳檔案用 | （含檔案二進制） |
| `text/plain` | 純文字 | `Hello World` |
| `text/html` | HTML 內容 | `<html>...</html>` |
| `application/xml` | XML 格式（老系統、SOAP） | `<user><name>Ryan</name></user>` |

---

## Authentication（身分驗證）

| 方式 | 怎麼帶 | 適用場景 |
|------|------|---------|
| **API Key** | `?api_key=xxx` 或 header `X-API-Key: xxx` | 簡單服務、第三方整合 |
| **Basic Auth** | header `Authorization: Basic base64(user:pass)` | 內部工具、舊系統 |
| **Bearer Token (JWT)** | header `Authorization: Bearer eyJhbGci...` | **目前最常見**，現代網站 / SPA |
| **OAuth 2.0** | 多步驟流程，最後拿 access token | 第三方登入（Google、Facebook） |
| **Session / Cookie** | 瀏覽器自動帶 cookie | 傳統網站 |

### JWT (JSON Web Token) — 最常見

長這樣：
```
eyJhbGciOiJIUzI1NiIs.eyJzdWIiOiIxMjM0NSIsImV4cCI6MTcxNDQ2MTQwMH0.SflKxwRJSMeKKF...
└─ Header (演算法)   └─ Payload (使用者資訊、過期時間)         └─ Signature (簽章)
```

QA 注意點：
- ✅ Token 過期該回 401（不是 500）
- ✅ Token 偽造該回 401
- ✅ 別人的 token 拿來用該怎麼擋（refresh token 機制）

---

## RESTful API 設計觀念

REST 是一套「**用 HTTP 設計 API 的慣例**」。設計良好的 API 長這樣：

| 操作 | URL | Method |
|------|-----|--------|
| 取得所有使用者 | `/users` | GET |
| 取得特定使用者 | `/users/123` | GET |
| 新增使用者 | `/users` | POST |
| 完整更新使用者 | `/users/123` | PUT |
| 部分更新使用者 | `/users/123` | PATCH |
| 刪除使用者 | `/users/123` | DELETE |
| 取得使用者的訂單 | `/users/123/orders` | GET |

### 常見壞味道（API 設計 anti-pattern）— QA 看到要報

❌ **動詞放在 URL 裡**：`/getUser`、`/deleteOrder` → 應該用 method 區分
❌ **GET 用來改資料**：`/users/delete?id=123` → 違反「GET 安全性」
❌ **狀態碼亂用**：明明是 404 卻回 200 + body 寫 `{"error": "not found"}`
❌ **錯誤訊息不一致**：有時 `error`、有時 `message`、有時 `errors`
❌ **回傳沒有 schema**：相同 endpoint 回不同結構

---

## QA 測試重點

### 1. Happy Path（正向測試）— 一切正常
```
POST /users  body={"name": "Ryan"}
→ 預期：201 Created + 回傳新建使用者資料
```

### 2. Negative Test（反向測試）— 該失敗時失敗
| 測試 | 預期回應 |
|------|---------|
| 缺必填欄位 | 400 |
| 格式錯誤的 email | 400 / 422 |
| Email 已存在 | 409 |
| 沒帶 token | 401 |
| Token 過期 | 401 |
| 權限不足 | 403 |
| 改別人的資料 | 403 |
| 改不存在的 ID | 404 |

### 3. Boundary Test（邊界測試）
- 字串長度：0 / 1 / 最大值 / 最大值+1
- 數字：負數 / 0 / 最大值 / 超過範圍
- 列表：空陣列 / 1 個 / 大量

### 4. Idempotency Test（冪等性測試）
- 同一個 PUT 呼叫 100 次，最終資料一樣
- 同一個 DELETE 呼叫兩次，第二次該回 404

### 5. Concurrency Test（並發測試）
- 兩個人同時改同一筆資料 → 預期會有 lock 或 version conflict（409）

### 6. Performance Test
- 平均回應時間 < 200ms
- P95 / P99 不能太誇張
- 工具：JMeter、k6、Locust

### 7. Security Test
- SQL Injection：`' OR '1'='1`
- XSS：`<script>alert(1)</script>`
- 路徑遍歷：`../../etc/passwd`
- 大量請求：被打掛之前該有 rate limit

### 8. Schema Validation（回應格式驗證）
驗證回傳 JSON 的結構符合預期 schema：
```python
import jsonschema

schema = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
    }
}
jsonschema.validate(instance=response_json, schema=schema)
```

### 9. Contract Test（合約測試）
前後端事先約定好 API 介面（OpenAPI / Swagger 文件），任一邊改了就要驗證沒破壞合約。工具：Pact、Spring Cloud Contract。

---

## Python `requests` 實作範例

### 基本 GET
```python
import requests

resp = requests.get("https://api.example.com/users/123")
print(resp.status_code)   # 200
print(resp.json())        # {"id": 123, "name": "Ryan"}
print(resp.headers)       # 回應的 headers
```

### 帶 Query Parameters
```python
resp = requests.get(
    "https://api.example.com/users",
    params={"page": 2, "size": 20}
)
# 等同打 https://api.example.com/users?page=2&size=20
```

### POST + JSON Body
```python
resp = requests.post(
    "https://api.example.com/users",
    json={"name": "Ryan", "email": "ryan@example.com"}
    # 用 json= 會自動 encode 成 JSON 並設定 Content-Type
)
```

### POST + 表單
```python
resp = requests.post(
    "https://api.example.com/login",
    data={"username": "ryan", "password": "1234"}
    # 用 data= 會以 x-www-form-urlencoded 送出
)
```

### 帶 Authentication
```python
# Bearer Token
headers = {"Authorization": "Bearer eyJhbGci..."}
resp = requests.get(url, headers=headers)

# Basic Auth
resp = requests.get(url, auth=("username", "password"))

# API Key (header)
headers = {"X-API-Key": "your-api-key"}
resp = requests.get(url, headers=headers)
```

### 上傳檔案
```python
with open("photo.jpg", "rb") as f:
    resp = requests.post(
        "https://api.example.com/upload",
        files={"file": f}
    )
```

### 設定 Timeout（業界必加）
```python
# (連線時間, 等待回應時間) 兩個 timeout
resp = requests.get(url, timeout=(3, 10))
```

### Session（重複利用連線、保留 cookie）
```python
with requests.Session() as session:
    # 1. 登入
    session.post(login_url, json={"user": "ryan", "pass": "1234"})
    # 2. 後續請求會自動帶上登入後的 cookie
    resp = session.get("https://api.example.com/me")
```

### 完整 QA 測試範例（pytest 風格）
```python
import requests
import pytest

BASE_URL = "https://api.example.com"

def test_create_user_success():
    """測試建立使用者成功"""
    payload = {"name": "Ryan", "email": "ryan@test.com"}
    resp = requests.post(f"{BASE_URL}/users", json=payload, timeout=10)

    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Ryan"
    assert body["email"] == "ryan@test.com"
    assert "id" in body
    assert "created_at" in body

def test_create_user_missing_email():
    """測試缺 email 應回 400"""
    resp = requests.post(f"{BASE_URL}/users", json={"name": "Ryan"})
    assert resp.status_code == 400
    assert "email" in resp.json()["error"].lower()

def test_create_user_duplicate_email():
    """測試 email 已存在應回 409"""
    payload = {"name": "Ryan", "email": "duplicate@test.com"}
    requests.post(f"{BASE_URL}/users", json=payload)  # 先建一筆
    resp = requests.post(f"{BASE_URL}/users", json=payload)
    assert resp.status_code == 409

def test_unauthorized():
    """沒帶 token 該回 401"""
    resp = requests.get(f"{BASE_URL}/me")
    assert resp.status_code == 401

@pytest.mark.parametrize("invalid_email", [
    "no-at-sign",
    "@no-username.com",
    "no-domain@",
    "",
])
def test_invalid_email_format(invalid_email):
    """各種無效 email 格式都該回 400"""
    resp = requests.post(
        f"{BASE_URL}/users",
        json={"name": "Ryan", "email": invalid_email}
    )
    assert resp.status_code == 400
```

---

## 業界常用工具

| 工具 | 用途 | 適合場景 |
|------|------|---------|
| **Postman** | GUI 工具測 API | 探索 API、寫測試集合 |
| **curl** | 命令列 | CI/CD、快速驗證 |
| **HTTPie** | 友善版 curl | 命令列但要好看 |
| **requests** (Python) | Python 自動化 | 寫測試腳本 |
| **pytest + requests** | Python 測試框架 | 大型 API 測試套件 |
| **REST Assured** (Java) | Java 測試框架 | Java 後端團隊 |
| **Swagger / OpenAPI** | API 文件 + 測試 | API 規格管理 |
| **JMeter / k6 / Locust** | 效能測試 | 壓測、負載測試 |
| **Newman** | Postman CLI | 把 Postman 集合放進 CI/CD |
| **Mock Server** (WireMock、json-server) | 假伺服器 | 後端還沒好就先測前端 |

---

## 常見問題排查

### `ConnectionError` / Timeout
- 網路斷了
- 伺服器掛了
- Firewall / VPN 擋住
- DNS 解析失敗
- → 用 `ping` / `curl` 確認伺服器活著

### `SSLError`
- 自簽憑證 → `requests.get(url, verify=False)`（**測試環境才能這樣，正式不要**）
- 系統憑證過期 → 更新作業系統

### 回 `403` 但確定有權限
- Token 帶錯（多空格、少 `Bearer ` 前綴）
- 環境搞錯（dev token 打 prod）
- IP 白名單沒設

### 回 `415 Unsupported Media Type`
- 沒帶 `Content-Type: application/json`
- 用 `data=` 而不是 `json=`

### 回 `429 Too Many Requests`
- 被限流，看 `Retry-After` header 等多久
- 加上指數退避 (exponential backoff) 重試

### JSON 解析失敗
```python
try:
    data = resp.json()
except requests.exceptions.JSONDecodeError:
    print("回應不是 JSON：", resp.text[:500])
    # 通常是後端回了 HTML 錯誤頁
```

---

## 進階觀念（業界知道更好）

### REST vs GraphQL vs gRPC
| 類型 | 特色 | 何時用 |
|------|------|------|
| REST | 用 HTTP method 對 resource，最普遍 | 一般 Web API |
| GraphQL | 一個 endpoint，查詢由 client 決定欄位 | 前端需求多變、降低過度抓取 |
| gRPC | 用 Protocol Buffer，效能好 | 微服務內部溝通 |
| WebSocket | 雙向長連線 | 即時通訊、聊天、推播 |

### 微服務常見概念
- **API Gateway**：所有外部請求的入口（Nginx、Kong、AWS API Gateway）
- **Service Mesh**：服務間溝通管理（Istio、Linkerd）
- **Circuit Breaker**：上游掛掉時自動斷開，避免雪崩
- **Retry / Backoff**：失敗自動重試，間隔愈來愈長

### CORS（跨來源資源共享）
瀏覽器才會碰到的限制（Postman / 後端互打不會）。
- 前端 `https://www.foo.com` 打 API `https://api.foo.com` → 不同 origin
- 後端必須回 `Access-Control-Allow-Origin` header
- QA 測前端時要驗 CORS 設定有沒有開對

### Rate Limiting / Throttling
- 一個 IP 每分鐘最多打 60 次
- 超過回 429
- 通常會帶 header：
  - `X-RateLimit-Limit: 60`
  - `X-RateLimit-Remaining: 59`
  - `X-RateLimit-Reset: 1714461400`

### Caching
- `Cache-Control: max-age=3600`（快取 1 小時）
- `ETag` / `If-None-Match`（內容沒變回 304）
- QA 測試時要小心快取：用 `Cache-Control: no-cache` 強制重新打

---

## 一張圖總結 QA 該檢查什麼

```
打 API 之前要想：
├─ Method 用對嗎？(POST 用 GET 會 405)
├─ URL 對嗎？(env、path、query)
├─ Header 帶齊嗎？(Auth、Content-Type)
└─ Body 格式對嗎？(JSON 結構)

收到 Response 要驗：
├─ Status Code 是預期的嗎？
├─ Body 結構符合 schema 嗎？
├─ 必要欄位都有嗎？
├─ 資料值合理嗎？(不能是 null、負數)
├─ 回應時間在 SLA 內嗎？
└─ Headers 有缺嗎？(X-Request-ID、Content-Type)
```

---

## 學習路徑建議

1. ✅ **基礎**：HTTP method、status code（你目前在這）
2. 🔜 **入門**：用 `requests` 打 API、處理 JSON
3. 🔜 **實戰**：用 `pytest + requests` 寫測試
4. 🔜 **進階**：JWT、OAuth、schema validation、效能測試
5. 🔜 **業界**：API Gateway、microservices、contract testing

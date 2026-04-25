# Python 套件：原生 vs 第三方

## 用「手機 App」來比喻

| | 原生套件 | 第三方套件 |
|---|--------|-----------|
| **比喻** | 手機買來內建的 App（時鐘、計算機、相機） | 自己去 Google Play / App Store 下載的 App（LINE、IG、Spotify） |
| **誰寫的** | Python 官方團隊 | 任何人都可以寫（個人、社群、公司） |
| **怎麼來** | 裝 Python 就送你 | 要自己 `pip install` 下載安裝 |

---

## 原生套件（標準函式庫 / Standard Library）

> **= Python 官方掛保證，裝 Python 就送你**

- 由 Python 官方維護
- 跟著 Python 一起發佈
- 不用安裝、可離線使用

**常見原生套件：**

| 套件 | 用途 |
|------|------|
| `time` | 計時、sleep |
| `sys` | 系統相關（命令列參數、退出程式） |
| `os` | 檔案、目錄、環境變數 |
| `pathlib` | 路徑處理（推薦，比 os.path 好用） |
| `re` | 正規表達式 |
| `json` | 處理 JSON 資料 |
| `argparse` | 解析命令列參數 |
| `urllib` | 抓網頁（原生版，比較囉嗦） |
| `datetime` | 日期時間 |
| `csv` | 處理 CSV 檔 |

**官方完整清單**：https://docs.python.org/3/library/

---

## 第三方套件（Third-party）

> **= 網路上其他人寫的，要自己 pip install**

- 任何人都可以寫，上傳到 **PyPI**（Python 套件商城）
- 從 PyPI 下載到本機才能用
- 安裝指令：`pip install 套件名`

**常見第三方套件：**

| 套件 | 作者背景 | 用途 |
|------|---------|------|
| `requests` | 個人工程師 Kenneth Reitz | 抓網頁（超紅，幾乎人人都用） |
| `selenium` | 開源社群 | 瀏覽器自動化 |
| `pandas` | 工程師 Wes McKinney | 資料分析（全球最紅） |
| `numpy` | 開源社群 | 數值運算 |
| `flask` | 個人工程師 Armin Ronacher | 網頁框架 |
| `beautifulsoup4` | 開源社群 | HTML 解析 |

> 任何人都能寫第三方套件！把自己寫的程式打包上傳 PyPI，全世界都能 `pip install`。

---

## 怎麼分辨一個套件是原生還是第三方？

### 方法 1：查官方文件
- 在 https://docs.python.org/3/library/ 上有的就是原生

### 方法 2：在 terminal 試
```bash
pip show requests   # 有輸出 → 第三方
pip show os         # 跳「Package(s) not found」→ 原生
```

### 方法 3：印出檔案位置
```python
import requests
import os
print(requests.__file__)  # 路徑含 site-packages → 第三方
print(os.__file__)        # 路徑在 Python/Lib 下 → 原生
```

---

## 為什麼要分這個？

| 情境 | 為什麼要 care |
|------|------------|
| **部署到其他電腦** | 第三方要在新電腦上 `pip install` 補回來；原生不用 |
| **`requirements.txt` 管理依賴** | 只列**第三方**套件，原生不用列 |
| **環境隔離（venv）** | 第三方裝在虛擬環境內，不汙染系統 |
| **公司資安政策** | 有些公司禁裝外部套件，要選原生替代方案 |

---

## 同一件事的「原生 vs 第三方」對比

### 抓網頁

**原生 `urllib`（Python 官方寫的）**
```python
from urllib.request import urlopen
url = "https://example.com"
response = urlopen(url)
html = response.read().decode("utf-8")
```
👆 有點囉嗦，但不用安裝

**第三方 `requests`（Kenneth Reitz 寫的）**
```python
import requests
html = requests.get("https://example.com").text
```
👆 一行解決，但要 `pip install requests`

### 其他常見對比

| 任務 | 原生做法 | 第三方做法 |
|------|---------|-----------|
| 解析 JSON | `json.loads()` | （原生就夠） |
| 處理日期 | `datetime` | `arrow`、`pendulum`（更人性化） |
| 表格 / CSV | `csv` | `pandas`（功能強很多） |
| HTML 解析 | 自己 split/find | `BeautifulSoup4`、`lxml` |

> **重要結論**：官方寫的不一定最好用，第三方寫的有時更香！

---

## 實際範例（神魔之塔爬蟲專案）

```python
# 原生（不用裝）
import time              # 計時、sleep
import sys               # 系統相關
import argparse          # 解析命令列參數
from pathlib import Path # 路徑處理

# 第三方（要 pip install）
import requests          # pip install requests
from selenium import webdriver  # pip install selenium
```

新電腦要跑這專案前，必須先：
```bash
pip install selenium requests brotli
```
（原生的 `time`、`sys`、`argparse`、`pathlib` 完全不用管）

---

## 安全性提醒（新手必看）

因為**任何人都能寫第三方套件**，理論上會有壞人上傳惡意套件。建議：

1. **看下載量、星星數** — 上 https://pypi.org 搜尋，看 GitHub 星星和下載量
2. **挑名氣大的** — `requests` 5.5 萬+ ⭐、`numpy`、`pandas` 用了多年沒事
3. **拼字小心** — 有壞人會註冊 `requets`（少一個 s）這種假套件騙人，看清楚名字
4. **公司專案** — 通常有白名單規定能裝哪些套件

---

## 一句話總結

> **原生** = Python 官方包進去的，內建。
> **第三方** = 開放給全世界寫並分享的，要自己 `pip install`。

Python 強大就強大在這個第三方生態系 —— **PyPI 上有 50 萬+ 個套件**，幾乎想做什麼都有人寫好了 😎

---

## 排錯小技巧

遇到 `ModuleNotFoundError: No module named 'xxx'`：

1. **如果是原生套件** → 拼字打錯了（例如 `import os` 不是 `import OS`）
2. **如果是第三方套件** → 還沒裝，要 `pip install xxx`
3. **如果是 venv 環境** → 確認你的 terminal 是不是在虛擬環境裡（前面會有 `(venv)`）

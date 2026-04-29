# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案背景

這是一個 Python 學習專案，依學習主題分資料夾管理，目前涵蓋三大主題：
1. **Python 基礎語法**（01_Basic_Learning）
2. **Selenium 網頁自動化**（02_Selenium_Learning）
3. **API 呼叫與 requests**（03_Api_Learning）

Side project 為實際應用練習：爬取巴哈姆特神魔之塔討論版的高 GP 回覆。

## 執行方式

安裝依賴：
```bash
pip install selenium requests brotli
```

執行爬蟲主程式（需從專案根目錄執行，否則 `sys.path` 會找不到 `utils/`）：
```bash
# 一般模式（會開啟 Chrome 視窗）
python side_projects/madhead_post_crawler_pro.py

# 無頭模式（背景執行，不開視窗）
python side_projects/madhead_post_crawler_pro.py --headless
```

執行 API 練習：
```bash
python 03_Api_Learning/01_http_methods.py
```

## 架構說明

### 兩份 `WebController`（注意區分）

| 路徑 | 用途 |
|------|------|
| `utils/drivers.py` | 課程練習用，無頭模式支援尚未加入 |
| `side_projects/utils/drivers.py` | Side project 用，支援 `headless` 參數與 `find_elements`、`close_windows` |

主程式 `madhead_post_crawler_pro.py` import 的是 `side_projects/utils/drivers.py`。

### 工具類別

- **`utils/file_manager.py` → `FileHandler`**：讀寫 txt / JSON 的共用工具。`save_txt()` 要求檔案必須預先存在（不會自動建立）。
- **`side_projects/utils/`**：side project 專屬版本的 `drivers.py`、`file_manager.py`、`logger.py`、`data_manager.py`。

### `sys.path` 注入

`madhead_post_crawler_pro.py` 開頭用 `pathlib.Path` 動態把專案根目錄加入 `sys.path`，讓 `from utils.xxx import xxx` 可以在任意目錄下執行。其他練習腳本沒有這個機制，需從根目錄執行。

### Log 檔

Log 存在 `side_projects/logs/`，`save_txt()` 寫入前會確認檔案是否存在，**不存在不會自動建立**，需手動預建空檔案。

## 開發注意事項

- 一個課程主題對應一個 PR（per-topic branch workflow）。
- 命名遵循 PEP8；變數命名偏好具體描述（`line_num` 優於 `num`）。
- function 都要有中文 docstring 說明用途與參數。
- 不使用 `time.sleep()`，改用 Selenium 的顯式等待（`WebDriverWait` + `EC`）。

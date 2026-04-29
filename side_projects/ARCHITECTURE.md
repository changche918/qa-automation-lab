# 神魔之塔爬蟲 - 系統架構圖

## 整體架構

```mermaid
flowchart TD
    User([使用者]) -->|"python madhead_main.py --mode api/web"| Main[madhead_main.py 程式入口]

    Main -->|"args.mode == 'api'"| APIMode{API 模式}
    Main -->|"args.mode == 'web'"| WebMode{Web 模式}

    %% API mode flow
    APIMode --> Finder1[FindHighGPApi<br>find_high_gp_with_api.py]
    Finder1 -->|"requests.get BOARD_URL"| ScanPostAPI[scan_high_gp_post_api]
    ScanPostAPI -->|"return titles, best_art_url"| LogPost1[file_path<br>madhead_post_log.txt]
    ScanPostAPI -->|"best_art_url"| ScanContentAPI[scan_high_gp_content_api]
    ScanContentAPI -->|"requests.get 每頁"| ScanContentAPI
    ScanContentAPI -->|"return content, has_next"| LogContent1[content_path<br>madhead_content_log.txt]

    %% Web mode flow
    WebMode --> Driver[WebController<br>drivers.py]
    Driver -->|"開啟 Chrome 載入 BOARD_URL"| Finder2[FindHighGPWeb<br>find_high_gp.py]
    Finder2 --> ScanPostWeb[scan_high_gp_post]
    ScanPostWeb -->|"return titles, best_art_elem"| LogPost2[file_path<br>madhead_post_log.txt]
    ScanPostWeb -->|"click 跳轉文章"| ScanContentWeb[scan_high_gp_content]
    ScanContentWeb -->|"找 next 按鈕後 click 翻頁"| ScanContentWeb
    ScanContentWeb -->|"return content"| LogContent2[content_path<br>madhead_content_log.txt]

    %% Shared
    LogPost1 -.使用.-> FileMgr[FileHandler<br>file_manager.py]
    LogPost2 -.使用.-> FileMgr
    LogContent1 -.使用.-> FileMgr
    LogContent2 -.使用.-> FileMgr

    %% Styling
    classDef apiStyle fill:#e1f5ff,stroke:#0277bd,stroke-width:2px
    classDef webStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef sharedStyle fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px
    classDef logStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px

    class APIMode,Finder1,ScanPostAPI,ScanContentAPI apiStyle
    class WebMode,Driver,Finder2,ScanPostWeb,ScanContentWeb webStyle
    class Main,FileMgr sharedStyle
    class LogPost1,LogPost2,LogContent1,LogContent2 logStyle
```

## 模組職責

| 模組 | 職責 |
|------|------|
| `madhead_main.py` | 程式入口；根據 `--mode` 參數切換 API / Web 模式 |
| `utils/find_high_gp_with_api.py` | API 模式：用 requests 抓 HTML，純字串解析 |
| `utils/find_high_gp.py` | Web 模式：用 Selenium 開瀏覽器互動 |
| `side_projects/utils/drivers.py` | Web 模式專用的 Chrome WebDriver 包裝 |
| `utils/file_manager.py` | 共用 log 寫入工具 |

## API 模式 vs Web 模式對照

| 項目 | API 模式 | Web 模式 |
|------|---------|---------|
| HTTP 請求 | `requests.get(url)` | Selenium 開 Chrome 載入 |
| 解析 HTML | 純字串 `split` / `find` | CSS selector + WebElement |
| 「點進文章」 | 拿 href → 換 URL 再 GET | `elem.click()` 真的點 |
| 翻頁 | 組 `&page={n}` URL 重新 GET | 找 `.next` 按鈕 click |
| 「下一頁」偵測 | 字串比對 `class="next"`/`'next'` | `find_elements(.next.no)` 數量 |
| 依賴 | 只需 `requests` | `selenium` + Chrome + driver |
| 執行成本 | 快、輕、可平行 | 慢、吃資源、會看到視窗 |
| JS 動態內容 | 抓不到 | 抓得到 |

## 執行方式

```bash
# API 模式（純 requests，不開瀏覽器）
python side_projects/madhead_main.py --mode api

# Web 模式（Selenium，會開 Chrome）
python side_projects/madhead_main.py --mode web
```

## 資料輸出

| Log 檔 | 內容 |
|--------|------|
| `side_projects/logs/madhead_post_log.txt` | 高 GP 文章標題清單 + 最高 GP 文章網址 |
| `side_projects/logs/madhead_content_log.txt` | 高 GP 回覆 + 爆文內文 |

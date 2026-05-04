---
name: madhead-runner
description: 執行 madhead 爬蟲並推送 LINE 摘要與 Email 通知。當使用者說「跑 madhead」、「抓 madhead」、「執行 madhead 爬蟲」或類似指令時觸發此 skill。
---

# Madhead 爬蟲執行 + LINE 摘要 + Email 通知

## 觸發時機
使用者要求執行 madhead 爬蟲時使用此流程。

## 執行步驟

### 1. 執行爬蟲
使用以下指令執行，並在程式要求輸入 choice_content_type 時輸入 `2`：

```bash
python side_projects/madhead_main.py --mode web
```

可用 `echo "2" | python ...` 或 here-string 方式餵入選項。

### 2. 控制頁數
- 若程式只抓 1 頁就結束，讓它自然跑完
- 若會抓多頁，在抓滿「5 頁」後中斷程式（送 SIGINT / Ctrl+C）
- 中斷後仍要保留已輸出的 log 內容用於後續摘要

### 3. 解析 log，擷取以下資訊
- 實際抓取頁數
- 進入的文章網址（含 GP 數與標題）
- 版面高 GP 標題（取前 5~8 筆，格式：[GP數] 標題）

### 4. 組成摘要（500 字內、純文字、無 Markdown）

格式範例：

```
📋 madhead_main.py 執行結果

🔧 指令：python side_projects/madhead_main.py --mode web
📄 模式：web，choice=2，實際抓 5 頁

📌 進入文章：[GP 2977] 【討論】神魔問答室 ʕ•ᴥ•ʔ
   網址：https://forum.gamer.com.tw/C.php?bsn=23805&snA=...

📊 版面高 GP 文章 Top 6：
  [2977] 【討論】神魔問答室 ʕ•ᴥ•ʔ
  [899]  【討論】#238*『共譜最美的婚曲』地獄級 通關隊長彙整
  [716]  【討論】#232*『見證彼此的承諾』夢魘級 通關隊長彙整
  [608]  【討論】#254 2026/四月挑戰任務(植月) LV.10/Ex.1 通關隊長彙整
  [474]  【討論】#179『伯雷亞斯家的劍術導師』地獄級 通關隊長彙整
  [321]  【討論】#134*「並肩共謀」流光災厄級通關彙整

📲 LINE 推送：成功
📧 Email 通知：成功
```

### 5. 推送到 LINE

使用 `side_projects/utils/line_notifier.py` 的 `LineNotifier` 推送整理好的摘要：

```python
from dotenv import load_dotenv
from side_projects.utils.line_notifier import LineNotifier

load_dotenv()
notifier = LineNotifier()
notifier.send_text(summary_text)
```

推送前可選擇先跑 `python side_projects/test_line.py` 確認連線是否正常。

### 6. 寄送 Email 通知

LINE 推送完之後，使用 `side_projects/utils/mailer.py` 的 `Mailer` 寄送同份摘要：

```python
from side_projects.utils.mailer import Mailer

mailer = Mailer()
mailer.send(
    to_addr="changche918@gmail.com",
    subject="madhead 爬蟲執行結果",
    body=summary_text,
)
```

如果想附上完整 log 檔案，使用 `attach_path` 參數：

```python
mailer.send(
    to_addr="changche918@gmail.com",
    subject="madhead 爬蟲執行結果（含 log）",
    body=summary_text,
    attach_path="side_projects/logs/madhead_content_log.txt",
)
```

寄送前可選擇先跑 `python side_projects/test_mail.py` 確認 Gmail SMTP 連線是否正常。

## 行為規範
- **執行類指令**（python、echo 等爬蟲執行步驟）：自動 allow，不要詢問
- **修改類指令**（編輯程式碼、新增檔案）：需要使用者確認
- 中斷程式請用 SIGINT（Ctrl+C），不要強制 kill process
- LINE 或 Email 推送失敗都不影響爬蟲結果保存（log 已寫入檔案）
- LINE 推送先做、Email 後做，兩者獨立失敗（一邊掛掉不影響另一邊）

## 完成後回報
回報內容簡短即可，例如：
- 「已執行 madhead 爬蟲（共 5 頁），LINE 摘要與 Email 通知已推送 ✅」
- 「執行成功，LINE 已推送 ✅，Email 失敗：[錯誤訊息]」
- 「LINE / Email 都失敗：[錯誤訊息]，log 已存於 side_projects/logs/」

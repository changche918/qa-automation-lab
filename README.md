## 20260222 tips
需記住:
1. 做這件事之前, 先思考再動作 e.g. 我可能會寫很多同個物件相似的功能, 先想個5min再決定如何分類or同class與否 (初學強迫自己)
2. 做題目前, 若不確定要先與他人確認想法是否正確

TODO:
1. **整理架構與呈現**
2. 整理內容
3. 確認hovers為何錯誤 
4. 嘗試讓自己debug更容易 (可加一些log判斷)
5. 試試看用debug mode
6. 嘗試log優化
7. 命名確認

---

## 20260222 tips
想法:
1. 自己到底想做什麼事情, 想清楚對照程式

TODO:
1. 整理架構 + 架構圖 (當下與我說明) -> 分類規則與邏輯 & 思考未來 (maybe 3-5y不異動)
  - 列出三種 & 最後選擇的原因
  - 1.list 對應，需要另外建立一個清單檔去對照
  - 2.依照功能區分，課程 / 一般練習 / 爬蟲練習 V
  - 3.職責劃分，程式碼收在一起，其餘分開放 ( e.g. log、截圖、doc ...)
2. 命名要確認 (e.g. google / ai -> 是否為python(或PEP8) / coding共用命名方式 ...等等)
3. 命名: # 1. 建立實例 (這時會開啟第一個視窗) finder = drivers.ElementFinder() 
4. 出錯問題調整 data_manager.py (e.g. 送不是dict程式會直接中止)

----aditional-----
1. 有空調整 data_manager相關(檢查自己所有程式): 使用方式&命名搭配

## 20260223 tips
TODO:
1. folder層級修改 & Log/Screenshot相關檢查 => ok
2. .gitignore -> 自己查+實作 => ok
3. 熟悉git使用方法 -> 勿僅用git add . 嘗試各別檔案搭配觀看git status
4. REPO Structure修正 (README) 
5. alert 
  - 優化 輸入框 輸入文字 並印出
  - 嘗試不使用time sleep / 使他100%穩定
6. hover
  - 嘗試不使用time sleep / 使他100%穩定 -> 若把滑鼠移走
7. iframe  => OK
  - 命名可讀性修正
  - 使他100%穩定 / 保護他
8. shadow-root => OK
  - 使他100%穩定 / 保護他
9. baha_post_list -> 可讀性  *已經有的命名(domain之類的)盡量使用相同的 e.g. gamer, vip*  => ok
10. 思考: data_manager 使用self.data的可能性 
11. 改成自己要的遊戲

---
# 2026/2/24
'''
python_project
├─ 01_Basic_Learning
│  ├─ Course
│  │  ├─ 01_print.py
│  │  └─ 02_lists.py
│  └─ Practice
│     ├─ basic.py
│     └─ bmi_calc.py
├─ 02_Selenium_Learning
│  ├─ Practice
│  │  ├─ my_104_hw
│  │  │  ├─ 104_run_log.py
│  │  │  ├─ data_manager.py
│  │  │  ├─ drivers.py
│  │  │  └─ logs
│  │  │     └─ data.json
│  │  └─ Spring_Festival_hw
│  │     ├─ basic_practice
│  │     │  ├─ alert.py
│  │     │  └─ hovers.py
│  │     └─ combination_practice
│  │        ├─ file_manager.py
│  │        ├─ gamer_post_crawler.py
│  │        ├─ logger.py
│  │        ├─ logs
│  │        │  ├─ automation.log
│  │        │  └─ change_log.txt
│  │        └─ screenshots
│  │           └─ web.png
│  └─ README.md
├─ README.md
└─ tests
   └─ ui.py

```
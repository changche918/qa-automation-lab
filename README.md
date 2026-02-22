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
  - 2.依照功能區分，課程 / 一般練習 / 爬蟲練習
  - 3.
2. 命名要確認 (e.g. google / ai -> 是否為python(或PEP8) / coding共用命名方式 ...等等)
3. 命名: # 1. 建立實例 (這時會開啟第一個視窗) finder = drivers.ElementFinder() 
4. 出錯問題調整 data_manager.py (e.g. 送不是dict程式會直接中止)

----aditional-----
1. 有空調整 data_manager相關(檢查自己所有程式): 使用方式&命名搭配
```
python_project
├─ automation.log
├─ change_log.txt
├─ error.png
├─ Practice_01
│  ├─ basic.py
│  └─ bmi_calc.py
├─ Python_Learning
│  ├─ 01_print
│  │  └─ 01_print.py
│  ├─ 02_lists
│  │  └─ 02_lists.py
│  ├─ 03_dictionaries
│  │  └─ 03_dictionaries.py
│  ├─ 04_if_else
│  │  └─ 04_if_else.py
│  ├─ 05_for_loop
│  │  └─ 05_for_loop.py
│  ├─ 06_functions
│  │  └─ 06_functions.py
│  ├─ 07_classes
│  │  ├─ 07_classes.py
│  │  ├─ boss_model
│  │  │  ├─ boss.py
│  │  │  ├─ boss_v1.py
│  │  │  ├─ boss_v2.py
│  │  │  └─ __pycache__
│  │  │     └─ boss.cpython-310.pyc
│  │  └─ my_project
│  │     ├─ A
│  │     │  ├─ aaa.py
│  │     │  └─ __pycache__
│  │     │     └─ aaa.cpython-310.pyc
│  │     ├─ bbb.py
│  │     ├─ ccc.py
│  │     └─ __pycache__
│  │        └─ bbb.cpython-310.pyc
│  ├─ 08_imports
│  │  └─ 08_imports.py
│  ├─ 09_try_except
│  │  └─ 09_try_except.py
│  └─ 10_file_handing
│     └─ 10_file_handing.py
├─ README.md
├─ Selenium_Practice
│  ├─ data.json
│  ├─ my_104_hw
│  │  ├─ 104_run_log.py
│  │  ├─ data_manager.py
│  │  ├─ drivers.py
│  │  └─ __pycache__
│  │     ├─ data_manager.cpython-310.pyc
│  │     └─ drivers.cpython-310.pyc
│  ├─ README.md
│  ├─ Spring_Festival_hw
│  │  ├─ basic_practice
│  │  │  ├─ alert.py
│  │  │  ├─ hovers.py
│  │  │  ├─ iframe.py
│  │  │  └─ shadow_root.py
│  │  ├─ combination_practice
│  │  │  ├─ baha_post_list.py
│  │  │  ├─ file_manager.py
│  │  │  ├─ logger.py
│  │  │  └─ __pycache__
│  │  │     ├─ file_manager.cpython-310.pyc
│  │  │     └─ logger.cpython-310.pyc
│  │  └─ __pycache__
│  │     ├─ file_manager.cpython-310.pyc
│  │     ├─ gen_log.cpython-310.pyc
│  │     ├─ logger.cpython-310.pyc
│  │     └─ log_manager.cpython-310.pyc
│  └─ __pycache__
│     ├─ conftest.cpython-310.pyc
│     ├─ driver.cpython-310.pyc
│     ├─ drivers.cpython-310.pyc
│     └─ gen_json.cpython-310.pyc
├─ ui.py
└─ web.png

```
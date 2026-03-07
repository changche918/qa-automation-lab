# 開發紀錄筆記

---
## 20260118

TODO: 
1. int, float, string的差異
2. 熟悉terminal各目錄執行
3. f-string用法

---
## 20260119

TODO: BMI運算並將結果存成list和dict 各一個程式

---
## 20260207

TODO: 
1. 到https://www.104.com.tw/網站 -> 找到五個區塊並逐一命名, 最少成印出文字+link(href)
    -> optimize hint: 能拆class/function | 能把區塊拆分更細 |
2. 存成txt檔案
    -> optimize hint: json格式的txt
---
## 20260209

TODO: 
1. 隱式等待與顯式等待 
2. 命名(可讀性) ex: text_1
3. debug "上市櫃"
4. **用迴圈嘗試**, 避免使用[0]這種
5. 修改json檔案的結構 hint: dict or list 
ex: 
  suit_job = {
    "適合你的好工作": {xxx}
  }
6. 抓元素可以嘗試用更清楚的 or 唯一值 or 不會變動的
7. 嘗試直接抓文字, 類似: text()="中高齡"

---
## 20260212

TODO: 
1. 正常版本會包含前面的code邏輯
2. 將第一版改為優化版
3. debug "上市櫃" (或換寫法)
4. (可讀性)
5. 物件建立方式
6. for迴圈盡量先少用一行用法 下方為sample
  `  data = {}
    for el in elements:
        `data[el.text] = el.get_attribute("href")
7. 單一職責 (思考功能拆分 盡量要單位小 **但不能過小**) 
8. DataSaver 還有什麼功能可以先預寫3個 裡面可以pass 有空的話寫簡單的內容
9. 嘗試不用XPATH抓 data-gtm-index 這些(可讀性)
10. 嘗試直接抓文字, 類似: text()="中高齡"

---
## 20260222

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
## 20260222

想法:
1. 自己到底想做什麼事情, 想清楚對照程式

TODO:
1. 整理架構 + 架構圖 (當下與我說明) -> 分類規則與邏輯 & 思考未來 (maybe 3-5y不異動)
    - 列出三種 & 最後選擇的原因
    - 1.list 對應，需要另外建立一個清單檔去對照
    - 2.依照功能區分，課程 / 一般練習 / 爬蟲練習
    - 3.職責劃分，程式碼收在一起，其餘分開放 ( e.g. log、截圖、doc ...)
2. 命名要確認 (e.g. google / ai -> 是否為python(或PEP8) / coding共用命名方式 ...等等)
3. 命名: # 1. 建立實例 (這時會開啟第一個視窗) finder = drivers.ElementFinder() 
4. 出錯問題調整 data_manager.py (e.g. 送不是dict程式會直接中止)

**aditional**
1. 有空調整 data_manager相關(檢查自己所有程式): 使用方式&命名搭配

---
## 20260223

TODO:
1. folder層級修改 & Log/Screenshot相關檢查
2. .gitignore -> 自己查+實作
3. 熟悉git使用方法 -> 勿僅用git add . 嘗試各別檔案搭配觀看git status
4. REPO Structure修正 (README) 
5. alert 
    - 優化 輸入框 輸入文字 並印出
    - 嘗試不使用time sleep / 使他100%穩定
6. hover
    - 嘗試不使用time sleep / 使他100%穩定 -> 若把滑鼠移走
7. iframe
    - 命名可讀性修正
    - 使他100%穩定 / 保護他
8. shadow-root
    - 使他100%穩定 / 保護他
9. baha_post_list -> 可讀性  *已經有的命名(domain之類的)盡量使用相同的 e.g. gamer, vip*
10. 思考: data_manager 使用self.data的可能性 
11. 改成自己要的遊戲

---
## 20260228

**下課後, 自行留10min整理上課重點與消化**
**上課前, 整理好想討論的項目 or 困惑的項目**

1. [x] 寫之前確認是否有相同的邏輯 or 用法
2. [ ] 若沒有, 思考要怎麼樣設計 
3. [ ] 寫完確認 (任何情況都要 -> 上傳前、上傳完成) 
4. [ ] 最外層README調整 & 思考呈現方式
5. [ ] alert Refactoring (e.g 區塊 or 開關)
6. [x] debug -> basic_practice (except)
7. [x] hover -> 驗證是否合理
8. [x] shadow_root -> 是否有方式替代find_element
9. [x] 共用driver (設計裡面) 

---
## 20260302

1. 歷程管理 & 日期 -> 設計
2. 推導過程 e.g. -> 單一符合 -> 多個符合 -> 邊界符合 (edge) or 其他情境 -> 找到最適合的方式(能解決你大部分的問題)

---
## 20260305

1. [] AI使用: 一次對話不要過多, 若太多可以拆分, 或是清除視窗再問(拆分單元的概念) -> new session 避免hallucination
2. [] AI不一定必須使用json / markdown格式才會比較清楚, 是因為你在使用這些格式的時候, 腦袋已經先整理清楚了 #輸出json會比較好做後續應用
3. [X] "not found" -> 相容性 -> stg staging -staging
    "Not Found" -> PM規定的文字 -> 完全不能有誤差
------
1. [?] 確認路徑為何不能使用, (可額外嘗試讓各路徑都可以執行)
2. [?] 都改共用driver + 哪邊可抽成function (e.g. wait.until(EC.element_to_be_clickable))
3. [] 減少重複code (e.g. driver.switch_to.default_content()) -> hint: 回到default狀態
4. [] 確認 inner_p = wait.until(lambda _: root.find_element(By.CSS_SELECTOR, "slot"))

筆記 : 
1. PEP8 規範要弄熟
2. 要知道程式用法，e.g. lower >>> 不在意大小寫， '==' >>> 完整比對
3. 一個課程一個 PR
# 03_104_run.log.py

<!-- # TODO: 
# 1. 正常版本會包含前面的code邏輯 
# 2. 將第一版改為優化版
# 3. debug "上市櫃" (或換寫法)
# 4. (可讀性)
# 5. 物件建立方式
# 6. for迴圈盡量先少用一行用法 下方為sample
#   `  data = {}
#     for el in elements:
#         `data[el.text] = el.get_attribute("href")
# 7. 單一職責 (思考功能拆分 盡量要單位小 **但不能過小**) 
# 8. DataSaver 還有什麼功能可以先預寫3個 裡面可以pass 有空的話寫簡單的內容
# 9. 嘗試不用XPATH抓 data-gtm-index 這些(可讀性)
# 10. 嘗試直接抓文字, 類似: text()="中高齡"


# ## 原先程式優化 ##
# 1. 需要知道每一行程式碼在尬麻
# 2. 讓程式碼不會有bug & 使用function 
#   ex: 
#     go_to_job_clinic_elem = function(xxx) -> function是什麼都行自行命名(可不同檔案或同檔案, 但不能在主程式practice_seleuium) 
# 3. driver抽出至另個檔案(function / class) **搭配2會有問題 (拿不到driver)**
# """ 

"""
TODO: 
1. 到https://www.104.com.tw/網站 -> 找到五個區塊並逐一命名, 最少成印出文字+link(href)
    -> optimize hint: 能拆class/function | 能把區塊拆分更細 |
2. 存成txt檔案
    -> optimize hint: json格式的txt
"""

-->
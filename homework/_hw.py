"""
## 基礎練習 ##
1. Hovers
    url = "https://the-internet.herokuapp.com/hovers"
    *target = hover user1 and click "View Profile"
    hint: Hovers

2. IFrame 處理
    url = https://the-internet.herokuapp.com/iframe
    *target = print: id="tinymce"'s text (Your content goes here.)
    hint: iframe

3. Alert / Confirm 對話框
    url = https://the-internet.herokuapp.com/javascript_alerts
    *target = click all btn, finally print (id="result")'s text
    hint: handle pop-up

4. shadow-root
    url = https://the-internet.herokuapp.com/shadowdom
    *target = print: name="my-text"'s text (My default text)
    hint: shadow-root

## 組合練習 ##
1. 偵測內容(範例: 第一個class=b-list__row b-list-item b-imglist-item有無更新, 此整行有無更新, 若有時間可嘗試更細的判斷)
    url = ex: https://forum.gamer.com.tw/B.php?bsn=84452
    要求: 
        1. 使用hint提及內容
        2. 將selenium driver獨立檔案使用(function)
        3. 當程式錯誤時, 當下截圖並存下(capture)
        4. 判斷重要資訊(人的帳號)是否更新或不同(.env), 環境變數使用ex: os.environ.get #此項真的做不出來沒關係
    每次執行時:
        - 確認log檔案是否存在: 
            - 不存在: 存下內容 | 存在: 對比差異
    若有不同:
        - 印出差異
        - 存下差異
        - 修改原先log
    hint: for loop, if-else, class, function, file-control(ex: with), os(for example)

## 原先程式優化 ##
1. 需要知道每一行程式碼在尬麻
2. 讓程式碼不會有bug & 使用function 
  ex: 
    go_to_job_clinic_elem = function(xxx) -> function是什麼都行自行命名(可不同檔案或同檔案, 但不能在主程式practice_seleuium) 
3. driver抽出至另個檔案(function / class) **搭配2會有問題 (拿不到driver)
"""


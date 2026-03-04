from selenium.webdriver.common.by import By
from utils.data_manager import DataManager
from utils.drivers import WebController

# 20260302 調整由最外層取得 data_manager & drivers function，
    # 執行須使用語法 : python -m 02_Selenium_Learning.Practice.my_104_hw.104_run_log 

# 1. 建立實例 (這時會開啟第一個視窗)
finder = WebController()

# 2. 前往目標網頁 (只需載入一次)
finder.get_url("https://www.104.com.tw/")

# 登入看專屬職缺
login_to_see_elem = finder.find_elem((By.XPATH, "//*[text()='登入看專屬職缺 ']")) # 傳入 Tuple (元組) 需要兩個 ((

# 地區找工作
area_to_find_elem = finder.find_elem((By.XPATH, "//*[text()='地區找工作']"))

# 上市櫃
listing_and_OTC_elem = finder.find_elem((By.XPATH, "//*[text()='上市櫃']"))

# 前往職涯診所
go_to_job_clinic_elem = finder.find_elem((By.XPATH, "//*[text()='前往職涯診所']"))

# 檢視職業適合度
view_job_fit_elem = finder.find_elem((By.XPATH, "//*[text()='檢視職業適合度']"))


job_type_dict = [
    login_to_see_elem,
    area_to_find_elem,
    listing_and_OTC_elem,
    go_to_job_clinic_elem,
    view_job_fit_elem
]

# job_results_dict =  {1, 2, 3, 4, 5} # 這行是拿來測試會進入 except 的用法
job_results_dict =  {}

for elem in job_type_dict:
    if elem: 
        name = elem.text
        link = elem.get_attribute("href")
        job_results_dict[name] = link

# 20260222
gen_json_json = DataManager(title="適合你的好工作")
gen_json_json.save(job_results_dict, "02_Selenium_Learning\Practice\my_104_hw\logs\data.json")

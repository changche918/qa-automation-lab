
from selenium.webdriver.common.by import By
import data_manager
import drivers


# 1. 建立實例 (這時會開啟第一個視窗)
finder = drivers.ElementFinder()

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

job_results_dict = {}

for elem in job_type_dict:
    if elem: 
        name = elem.text
        link = elem.get_attribute("href")
        job_results_dict[name] = link

gen_json_json = data_manager.DataSaver(title="適合你的好工作")
gen_json_json.save(job_results_dict, "selenium\data.json")
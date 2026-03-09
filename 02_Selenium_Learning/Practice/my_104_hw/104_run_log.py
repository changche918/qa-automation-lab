from selenium.webdriver.common.by import By
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..",".."))
sys.path.append(project_root)

from utils.drivers import WebController
from utils.data_manager import DataManager

finder = WebController()
finder.get_url("https://www.104.com.tw/")


# 20260302 調整由最外層取得 data_manager & drivers function，PR #4
# 20260307 刪除多餘註解，套用 function PR #7


# 登入看專屬職缺
login_to_see_elem = finder.wait_element_visible(By.XPATH, "//*[text()='登入看專屬職缺 ']") 

# 地區找工作
area_to_find_elem = finder.wait_element_visible(By.XPATH, "//*[text()='地區找工作']")

# 上市櫃
listing_and_OTC_elem = finder.wait_element_visible(By.XPATH, "//*[text()='上市櫃']")

# 前往職涯診所
go_to_job_clinic_elem = finder.wait_element_visible(By.XPATH, "//*[text()='前往職涯診所']")

# 檢視職業適合度
view_job_fit_elem = finder.wait_element_visible(By.XPATH, "//*[text()='檢視職業適合度']")


job_type_dict = [
    login_to_see_elem,
    area_to_find_elem,
    listing_and_OTC_elem,
    go_to_job_clinic_elem,
    view_job_fit_elem
]

job_results_dict =  {}

for elem in job_type_dict:
    if elem: 
        name = elem.text
        link = elem.get_attribute("href")
        job_results_dict[name] = link

gen_json_json = DataManager(title="適合你的好工作") 
gen_json_json.save(job_results_dict, "02_Selenium_Learning\Practice\my_104_hw\logs\data.json")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(project_root)

from utils.file_manager import FileHandler

file_path = "side_projects/logs/madhead_log.txt"
log = FileHandler()

class FindHighGP:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def scan_high_gp_content(self):
        page_best_gp = -1
        page_best_content = "無內容"

        # 1. 確保這頁樓層載入
        posts = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "section[id^='post_']")))

        # 2. 掃描本頁所有樓層
        for post in posts:
            gp_elements = post.find_elements(By.CSS_SELECTOR, ".postgp")
            
            if gp_elements:
                gp_text = gp_elements[0].text.strip()

                if "爆" in gp_text:
                    gp_value = 99999
                else:
                    # AI 提供 - 只保留數字，過濾掉非數字字元
                    clean_gp = "".join(filter(str.isdigit, gp_text))
                    gp_value = int(clean_gp) if clean_gp else 0

                    if gp_value > page_best_gp:
                        page_best_gp = gp_value
                        try:
                            page_best_content = post.find_element(By.CSS_SELECTOR, ".c-article__content").text
                        except:
                            page_best_content = "無法取得內文"

                # print(f"找到 GP: {gp_text}")
            else:
                print("此樓層找不到 GP 標籤，跳過")

        print(f"本頁最高 GP 為: {page_best_gp}")
        print(f"內容摘要:\n{page_best_content}...") # 只印前100字避免洗版
        log.save_txt(file_path, page_best_content)
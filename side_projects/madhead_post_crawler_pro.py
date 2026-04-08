from selenium.webdriver.common.by import By
import time
import sys

from pathlib import Path
from utils.find_high_gp import FindHighGP
import argparse

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.file_manager import FileHandler
from side_projects.utils.drivers import WebController

# log 路徑寫法 (1)
# file_path = "side_projects/logs/madhead_post_log.txt"
# content_path = "side_projects/logs/madhead_content_log.txt"

# log 路徑寫法 (2)
log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"

file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

# log 路徑寫法 (3)，Path(__file__) 目前檔案位置，.resolve() = 絕對路徑，parent = 上一層資料夾
# log_dir = Path(__file__).resolve().parent / "logs" 
# file_path = log_dir / "madhead_post_log.txt"
# content_path = log_dir / "madhead_content_log.txt"

# 執行無頭模式的設定
parser = argparse.ArgumentParser() # 我要開始定義這支程式可以吃哪些參數
parser.add_argument("--headless", action="store_true") # 只要你有打 --headless，就幫你設成 True
args = parser.parse_args() # 把你在 terminal 打的東西解析成變數 (--headless = True)

log = FileHandler()
driver_control = WebController(headless=args.headless) # 用使用者指定的模式，去建立一個瀏覽器控制器

# 20260322 初版 PR #10
# 20260324 調整程式寫法，使其可以取分頁 + GP PR #10
# 20260326 調整程式寫法，log.save 邏輯 PR #11
# 20260329 調整爆的寫法 PR #11
# 20260402 調整 log 路徑寫法，增加無頭模式，增加選擇執行模式 PR #12
# 20260404 調整 log 路徑寫法，args 可讀性調整、依照使用者選擇模式執行 PR #12

# 真實專案要爬的頁面
driver_control.get_url("https://forum.gamer.com.tw/C.php?bsn=23805&snA=729963&tnum=31")

# 1:取出第一筆爆的文章標題 或 2:取出所有爆的文章標題 (這行限定放在主程式)
choice_content_type = input("\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): ").strip() 

finder = FindHighGP(driver_control.driver)
# titles, best_art_elem = finder.scan_high_gp_post()
# log.save_txt(file_path, titles)

# if best_art_elem:
#     best_art_elem.click()

#     time.sleep(3)

#     current_page_url = driver_control.get_current_url()
#     log.save_txt(file_path, [f"文章網址: {current_page_url}"])

# finder.scan_high_gp_content()  # 進到巴哈人氣最高文章後的第一頁，爬取人氣最高回覆
best_text = finder.scan_high_gp_content(choice_content_type)
log.save_txt(content_path, best_text)

# 以下是換頁後 + 找到那頁 GP 最高的回覆文
while True:  # 使用無窮迴圈判斷切換分頁，滿足條件就跳出
    btns = driver_control.find_elements(By.CSS_SELECTOR, ".next")  # 下一頁的按鈕元素 (是 list)
    no_next_button = driver_control.find_elements(By.CSS_SELECTOR, ".next.no")  # 沒有下一頁的按鈕元素 (是 list)

    # 判斷 list 是否有東西
    if len(btns) > 0 and len(no_next_button) == 0:
        next_btn = btns[0]
        next_btn.click()
        time.sleep(5)
        print("換頁成功")
        best_text = finder.scan_high_gp_content(choice_content_type)
        log.save_txt(content_path, best_text)

    else:
        print("完全找不到下一頁按鈕，停止")
        
        break

driver_control.close_windows()

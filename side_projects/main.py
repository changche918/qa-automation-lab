import argparse
import requests
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

log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"

file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

log = FileHandler()

# 1. 建立參數解析器
parser = argparse.ArgumentParser(description="爬蟲與 API 執行工具")
parser.add_argument('--mode', choices=['api', 'web'], required=True, help="執行模式")
args = parser.parse_args()

# 2. 根據 mode 參數直接執行邏輯
if args.mode == 'api':
    # --- 這裡放跑 API 的程式碼 ---
    print("🚀 正在執行 API 模式...")
    # 例如：啟動你的伺服器
    # app.run() 

elif args.mode == 'web':
    # 真實專案要爬的頁面
    driver_control = WebController()
    driver_control.get_url("https://forum.gamer.com.tw/C.php?bsn=23805&snA=729963&tnum=31")

    # 1:取出第一筆爆的文章標題 或 2:取出所有爆的文章標題 (這行限定放在主程式)
    choice_content_type = input(
        "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
    ).strip()

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

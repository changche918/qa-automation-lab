import time
import sys
import argparse
from selenium.webdriver.common.by import By

from pathlib import Path
from utils.find_high_gp_with_api import FindHighGP as FindHighGPApi
from utils.find_high_gp import FindHighGP as FindHighGPWeb

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.file_manager import FileHandler
from side_projects.utils.drivers import WebController

# log 路徑
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
    print("執行 API 模式")

    # 版面列表頁（給 scan_high_gp_post_api 用）
    BOARD_URL = "https://forum.gamer.com.tw/B.php?bsn=23805"

    # 1:取出第一筆爆的回覆文 或 2:取出所有爆的回覆文 (這行限定放在主程式)
    choice_content_type = input(
        "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
    ).strip()

    finder = FindHighGPApi()

    # ── 1. 掃「版面列表頁」→ 用 BOARD_URL，同時拿到本頁 GP 最高文章的網址 ──
    titles, best_art_url = finder.scan_high_gp_post_api(BOARD_URL)
    log.save_txt(file_path, titles)

    print(best_art_url)
    # https://forum.gamer.com.tw/C.php?bsn=23805&snA=610529&tnum=23154
    # https://forum.gamer.com.tw/C.php?page=2&bsn=23805&snA=610529&tnum=23154

    if best_art_url:
        # 記錄「點進去」的文章網址，對應原本 Selenium 版 get_current_url() 的寫法
        log.save_txt(file_path, [f"文章網址: {best_art_url}"])

        # ── 2. 掃「本頁 GP 最高那篇文章」的回覆 ──
        best_text, has_next = finder.scan_high_gp_content_api(best_art_url, choice_content_type)

        log.save_txt(content_path, best_text)

        # 以下是換頁後 + 找到那頁 GP 最高的回覆文
        # ── 3. 換頁迴圈也是接在 best_art_url 後面（因為還在同一篇文章，只是翻頁）──
        page = 1
        while True:
            if has_next:
                page += 1
                next_url = f"{best_art_url}&page={page}"
                time.sleep(1)
                print("換頁成功")
                best_text, has_next = finder.scan_high_gp_content_api(next_url, choice_content_type)
                log.save_txt(content_path, best_text)
            else:
                print("完全找不到下一頁按鈕，停止")
                break

elif args.mode == 'web':
    print("執行 Web 模式")
    driver_control = WebController()

    # 真實專案要爬的頁面
    # driver_control.get_url("https://forum.gamer.com.tw/C.php?bsn=23805&snA=729963&tnum=31")
    driver_control.get_url("https://forum.gamer.com.tw/B.php?bsn=23805")

    # 1:取出第一筆爆的文章標題 或 2:取出所有爆的文章標題 (這行限定放在主程式)
    choice_content_type = input(
        "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
    ).strip()

    finder = FindHighGPWeb(driver_control.driver)
    titles, best_art_elem = finder.scan_high_gp_post()
    log.save_txt(file_path, titles)

    if best_art_elem:
        best_art_elem.click()

        time.sleep(3)

        current_page_url = driver_control.get_current_url()
        log.save_txt(file_path, [f"文章網址: {current_page_url}"])

    finder.scan_high_gp_content(choice_content_type)  # 進到巴哈人氣最高文章後的第一頁，爬取人氣最高回覆
    best_text = finder.scan_high_gp_content(choice_content_type)

    log.save_txt(content_path, best_text)

    # 以下是換頁後 + 找到那頁 GP 最高的回覆文
    page_count = 1  # 第一頁已爬完
    MAX_PAGES = 5
    while True:  # 使用無窮迴圈判斷切換分頁，滿足條件就跳出
        if page_count >= MAX_PAGES:
            print(f"已達最大頁數限制（{MAX_PAGES} 頁），停止")
            break

        btns = driver_control.find_elements(
            By.CSS_SELECTOR, ".next"
        )  # 下一頁的按鈕元素 (是 list)
        no_next_button = driver_control.find_elements(
            By.CSS_SELECTOR, ".next.no"
        )  # 沒有下一頁的按鈕元素 (是 list)

        # 判斷 list 是否有東西
        if len(btns) > 0 and len(no_next_button) == 0:
            next_btn = btns[0]
            next_btn.click()
            time.sleep(5)
            page_count += 1
            print(f"換頁成功（第 {page_count} 頁）")
            best_text = finder.scan_high_gp_content(choice_content_type)
            log.save_txt(content_path, best_text)

        else:
            print("完全找不到下一頁按鈕，停止")

            break

    driver_control.close_windows()


# ============== 以下是純 API 版本 ==============

"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.file_manager import FileHandler
from utils.find_high_gp_with_api import FindHighGP

# log 路徑寫法 (1)
# file_path = "side_projects/logs/madhead_post_log.txt"
# content_path = "side_projects/logs/madhead_content_log.txt"

# log 路徑寫法 (2)
log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"

file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

# 20260322 初版 PR #10
# 20260324 調整程式寫法，使其可以取分頁 + GP PR #10
# 20260326 調整程式寫法，log.save 邏輯 PR #11
# 20260329 調整爆的寫法 PR #11
# 20260402 調整 log 路徑寫法，增加無頭模式，增加選擇執行模式 PR #12
# 20260404 調整 log 路徑寫法，args 可讀性調整、依照使用者選擇模式執行 PR #12
# 20260422 改為純 API 版：移除 Selenium，改用 page 參數切換分頁

# 真實專案要爬的文章頁（不含 page，統一用迴圈補）
ARTICLE_URL = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=729963&tnum=31"

# 1:取出第一筆爆的回覆文 或 2:取出所有爆的回覆文
choice_content_type = input(
    "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
).strip()

log = FileHandler()
finder = FindHighGP()

page = 1
while True:
    # 組合每一頁的網址
    if page == 1:
        url = ARTICLE_URL
    else:
        url = f"https://forum.gamer.com.tw/C.php?page={page}&bsn=23805&snA=729963&tnum=31"

    # 掃本頁的高 GP 回覆；回傳 (清單, 是否還有下一頁)
    best_text, has_next = finder.scan_high_gp_content_api(url, choice_content_type)
    print(f"第 {page} 頁結果：{best_text}")
    log.save_txt(content_path, best_text)

    # 判斷是否還有下一頁；沒有就結束
    if not has_next:
        print("已經是最後一頁，停止")
        break

    page += 1
    time.sleep(1)  # 禮貌延遲

"""

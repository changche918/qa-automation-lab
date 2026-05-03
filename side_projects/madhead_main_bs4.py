# Created: 2026-05-03
import time
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from selenium.webdriver.common.by import By

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.file_manager import FileHandler
from side_projects.utils.drivers import WebController
from side_projects.utils.mailer import Mailer
from side_projects.utils.find_high_gp_with_api_bs4 import FindHighGP as FindHighGPApi
from side_projects.utils.find_high_gp import FindHighGP as FindHighGPWeb

# log 路徑
log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"

file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

log = FileHandler()

parser = argparse.ArgumentParser(description="爬蟲與 API 執行工具（API 模式改用 bs4）")
parser.add_argument("--mode", choices=["api", "web"], required=True, help="執行模式")
args = parser.parse_args()

if args.mode == "api":
    print("執行 API 模式（bs4 版）")

    BOARD_URL = "https://forum.gamer.com.tw/B.php?bsn=23805"

    choice_content_type = input(
        "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
    ).strip()

    finder = FindHighGPApi()

    titles, best_art_url = finder.scan_high_gp_post_api(BOARD_URL)
    log.save_txt(file_path, titles)

    print(best_art_url)

    print(f"[診斷] titles 數量: {len(titles)}")
    print(f"[診斷] titles 內容: {titles}")
    print(f"[診斷] best_art_url: {best_art_url}")


    all_content = []                        # ← 新增：累積每頁的回覆
    if best_art_url:
        log.save_txt(file_path, [f"文章網址: {best_art_url}"])

        best_text, has_next = finder.scan_high_gp_content_api(
            best_art_url, choice_content_type
        )
        log.save_txt(content_path, best_text)
        all_content.extend(best_text)


        page = 1
        while True:
            if has_next:
                page += 1
                next_url = f"{best_art_url}&page={page}"
                time.sleep(1)
                print("換頁成功")
                best_text, has_next = finder.scan_high_gp_content_api(
                    next_url, choice_content_type
                )
                log.save_txt(content_path, best_text)
                all_content.extend(best_text)  # ← 新增
                
                print(f"[診斷] 第 {page} 頁 best_text 數量: {len(best_text)}")
            else:
                print("完全找不到下一頁按鈕，停止")
                break


elif args.mode == "web":
    print("執行 Web 模式")
    driver_control = WebController()

    driver_control.get_url("https://forum.gamer.com.tw/B.php?bsn=23805")

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

    finder.scan_high_gp_content(choice_content_type)
    best_text = finder.scan_high_gp_content(choice_content_type)

    log.save_txt(content_path, best_text)

    page_count = 1
    MAX_PAGES = 5
    while True:
        if page_count >= MAX_PAGES:
            print(f"已達最大頁數限制（{MAX_PAGES} 頁），停止")
            break

        btns = driver_control.find_elements(By.CSS_SELECTOR, ".next")
        no_next_button = driver_control.find_elements(By.CSS_SELECTOR, ".next.no")

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

# ── 寄信 ──
try:
    # 直接從記憶體拿這次跑的結果，不從檔案讀（避免 log 累積）
    post_section = "\n".join(titles) if titles else "（無）"
    content_section = "\n".join(all_content) if all_content else "（無）"

    body = (
        "===== 版面高 GP 文章清單 =====\n"
        f"{post_section}\n\n"
        f"進入文章網址: {best_art_url or '（無）'}\n\n"
        "===== 文章內高 GP 回覆 =====\n"
        f"{content_section}"
    )

    Mailer().send(
        to_addr="changche918@gmail.com",
        subject=f"[巴哈神魔之塔] {args.mode.upper()} 模式爬取結果",
        body=body,
        attach_path=content_path,
    )
    print("郵件寄送成功")
except Exception as e:
    print(f"郵件寄送失敗：{e}")


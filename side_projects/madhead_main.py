import time
import sys
import time
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import argparse
import argparse
from selenium.webdriver.common.by import By

from pathlib import Path
from utils.find_high_gp_with_api import FindHighGP as FindHighGPApi
from utils.find_high_gp import FindHighGP as FindHighGPWeb

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from utils.file_manager import FileHandler
from side_projects.utils.drivers import WebController
from side_projects.utils.mailer import Mailer
from side_projects.utils.line_notifier import LineNotifier

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

# 通知用：跨模式收集結果（LINE / Email 共用）
all_content = []
article_url = None
titles = []

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
        article_url = best_art_url

        # 記錄「點進去」的文章網址，對應原本 Selenium 版 get_current_url() 的寫法
        log.save_txt(file_path, [f"文章網址: {best_art_url}"])

        # ── 2. 掃「本頁 GP 最高那篇文章」的回覆 ──
        best_text, has_next = finder.scan_high_gp_content_api(best_art_url, choice_content_type)

        log.save_txt(content_path, best_text)
        all_content.extend(best_text)

        # 以下是換頁後 + 找到那頁 GP 最高的回覆文
        # ── 3. 換頁迴圈也是接在 best_art_url 後面（因為還在同一篇文章，只是翻頁）──
        page = 1
        MAX_PAGES = 5
        while True:
            if has_next:
                if page >= MAX_PAGES:
                    print(f"已達最大頁數限制（{MAX_PAGES} 頁），停止")
                    break
                page += 1
                next_url = f"{best_art_url}&page={page}"
                time.sleep(1)
                print("換頁成功")
                best_text, has_next = finder.scan_high_gp_content_api(next_url, choice_content_type)
                log.save_txt(content_path, best_text)
                all_content.extend(best_text)
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
        article_url = current_page_url
        log.save_txt(file_path, [f"文章網址: {current_page_url}"])

    finder.scan_high_gp_content(choice_content_type)  # 進到巴哈人氣最高文章後的第一頁，爬取人氣最高回覆
    best_text = finder.scan_high_gp_content(choice_content_type)

    log.save_txt(content_path, best_text)
    all_content.extend(best_text)

    # 以下是換頁後 + 找到那頁 GP 最高的回覆文
    page_count = 1  # 第一頁已爬完
    MAX_PAGES = 5 
    while True:  # 使用無窮迴圈判斷切換分頁，滿足條件就跳出
        if page_count >= MAX_PAGES: # 這個是放在 AI 上跑，怕跑太多頁，所以先設定 5
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
            all_content.extend(best_text)

        else:
            print("完全找不到下一頁按鈕，停止")

            break

    driver_control.close_windows()


# ── 發送通知（LINE + Email，互相獨立）──
top_board = titles[:8] if titles else []
top_content = all_content[:8] if all_content else []
board_lines = "\n".join(top_board) if top_board else "（無）"
content_lines = "\n".join(top_content) if top_content else "（無）"

summary = f"""[巴哈神魔之塔] {args.mode.upper()} 模式爬取結果

進入文章網址:
{article_url or "（無）"}

版面高 GP 標題（前 {len(top_board)} 筆）:
{board_lines}

回覆高 GP 清單（前 {len(top_content)} 筆）:
{content_lines}"""

print("\n===== 通知摘要 =====")
print(summary.encode('utf-8', errors='replace').decode('utf-8'))
print("====================\n")

# LINE 推送
try:
    LineNotifier().send_text(summary)
    print("LINE 推送成功")
except Exception as e:
    print(f"LINE 推送失敗：{e}")

# Email 寄送
try:
    Mailer().send(
        to_addr="changche918@gmail.com",
        subject=f"[巴哈神魔之塔] {args.mode.upper()} 模式爬取結果",
        body=summary,
        attach_path=content_path,
    )
    print("Email 推送成功")
except Exception as e:
    print(f"Email 推送失敗：{e}")
# Created: 2026-05-03
"""排程任務執行腳本：API 模式爬取巴哈高 GP 文章，最多 5 頁，並發送 LINE 摘要通知。"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

from side_projects.utils.find_high_gp_with_api import FindHighGP
from side_projects.utils.line_notifier import LineNotifier
from side_projects.utils.mailer import Mailer
from utils.file_manager import FileHandler

BOARD_URL = "https://forum.gamer.com.tw/B.php?bsn=23805"
CHOICE = "2"  # 取出所有爆的回覆文
MAX_PAGES = 5

log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"
file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

log = FileHandler()
finder = FindHighGP()

print("執行 API 模式（排程任務）")

# ── 1. 掃版面列表頁 ──
print(f"掃描版面列表頁: {BOARD_URL}")
titles, best_art_url = finder.scan_high_gp_post_api(BOARD_URL)
log.save_txt(file_path, titles)

print(f"版面高 GP 文章清單：{titles}")
print(f"最高 GP 文章網址：{best_art_url}")

# ── 2. 進入最高 GP 文章，逐頁抓回覆 ──
all_content = []
pages_scraped = 0
article_url_logged = None

if best_art_url:
    log.save_txt(file_path, [f"文章網址: {best_art_url}"])
    article_url_logged = best_art_url

    # 第 1 頁
    pages_scraped = 1
    best_text, has_next = finder.scan_high_gp_content_api(best_art_url, CHOICE)
    log.save_txt(content_path, best_text)
    all_content.extend(best_text)
    print(f"第 1 頁爬取完成，has_next={has_next}")

    # 第 2～5 頁
    page = 1
    while has_next and pages_scraped < MAX_PAGES:
        page += 1
        pages_scraped += 1
        next_url = f"{best_art_url}&page={page}"
        time.sleep(1)
        print(f"換頁，抓第 {pages_scraped} 頁: {next_url}")
        best_text, has_next = finder.scan_high_gp_content_api(next_url, CHOICE)
        log.save_txt(content_path, best_text)
        all_content.extend(best_text)
        print(f"第 {pages_scraped} 頁爬取完成，has_next={has_next}")

    if pages_scraped >= MAX_PAGES and has_next:
        print(f"已達最大頁數限制（{MAX_PAGES} 頁），停止")
    elif not has_next:
        print("完全找不到下一頁按鈕，停止")
else:
    print("找不到最高 GP 文章，程式結束")

# ── 3. 整理 LINE 摘要 ──
top_board = titles[:8] if titles else []
top_content = all_content[:8] if all_content else []

board_lines = "\n".join(top_board) if top_board else "（無）"
content_lines = "\n".join(top_content) if top_content else "（無）"

summary = f"""[巴哈神魔之塔] 每日高 GP 摘要
執行指令: python side_projects/madhead_main.py --mode api
選擇模式: 2（取出所有爆的回覆文標題）
實際抓取頁數: {pages_scraped}

進入文章網址:
{article_url_logged or "（無）"}

版面高 GP 標題清單（前 {len(top_board)} 筆）:
{board_lines}

回覆高 GP 清單（前 {len(top_content)} 筆）:
{content_lines}"""

print("\n===== LINE 摘要內容 =====")
print(summary)
print("=========================\n")

# ── 4. 發送 LINE 通知 ──
line_success = False
try:
    notifier = LineNotifier()
    notifier.send_text(summary)
    line_success = True
    print("LINE 推送成功")
except Exception as e:
    print(f"LINE 推送失敗：{e}")

print(f"LINE 推送是否成功: {line_success}")

# ── 5. 發送 Email 通知 ──
mail_success = False
try:
    Mailer().send(
        to_addr="changche918@gmail.com",
        subject="[巴哈神魔之塔] 每日高 GP 摘要",
        body=summary,
        attach_path=content_path,
    )
    mail_success = True
    print("Email 推送成功")
except Exception as e:
    print(f"Email 推送失敗：{e}")

print(f"Email 推送是否成功: {mail_success}")

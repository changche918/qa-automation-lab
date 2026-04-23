import time
import sys

from pathlib import Path
from utils.find_high_gp_with_api import FindHighGP

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.file_manager import FileHandler

# log 路徑
log_dir = "side_projects/logs/madhead_"
file_extension = "log.txt"

file_path = f"{log_dir}post_{file_extension}"
content_path = f"{log_dir}content_{file_extension}"

log = FileHandler()

# 版面列表頁（給 scan_high_gp_post_api 用）
BOARD_URL = "https://forum.gamer.com.tw/B.php?bsn=23805"

# 1:取出第一筆爆的回覆文 或 2:取出所有爆的回覆文 (這行限定放在主程式)
choice_content_type = input(
    "\n請輸入編號選擇功能 (1:取出第一筆爆的回覆文標題 或 2:取出所有爆的回覆文標題): "
).strip()

finder = FindHighGP()

# ── 1. 掃「版面列表頁」→ 用 BOARD_URL，同時拿到本頁 GP 最高文章的網址 ──
titles, best_art_url = finder.scan_high_gp_post_api(BOARD_URL)
log.save_txt(file_path, titles)

print(best_art_url)

if best_art_url:
    # 記錄「點進去」的文章網址，對應原本 Selenium 版 get_current_url() 的寫法
    log.save_txt(file_path, [f"文章網址: {best_art_url}"])

    # ── 2. 掃「本頁 GP 最高那篇文章」的回覆 ──
    best_text, has_next = finder.scan_high_gp_content_api(best_art_url, choice_content_type)
    print(best_text)
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

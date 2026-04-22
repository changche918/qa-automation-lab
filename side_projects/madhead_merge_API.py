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

    # 抓 HTML（只抓一次，後續判斷下一頁也用這份）
    html_text = finder.fetch_html(url)

    # 解析本頁高 GP 回覆
    best_text = finder._parse_content(html_text, choice_content_type)
    print(f"第 {page} 頁結果：{best_text}")
    log.save_txt(content_path, best_text)

    # 判斷是否還有下一頁；沒有就結束
    if not finder.has_next_page(html_text):
        print("已經是最後一頁，停止")
        break

    page += 1
    time.sleep(1)  # 禮貌延遲，避免被擋

# Created: 2026-04-16
"""巴哈爬蟲 → Claude 摘要 → LINE 推送 主流程。

執行方式（本機測試）：
    python side_projects/pipeline.py --headless

跳過摘要／LINE 單獨除錯：
    python side_projects/pipeline.py --headless --no-summarize
    python side_projects/pipeline.py --headless --no-line
"""
import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from selenium.webdriver.common.by import By

# 讓這支檔案不管從哪裡被呼叫都能找到 side_projects.*
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from side_projects.utils.ai_summarizer import AISummarizer
from side_projects.utils.drivers import WebController
from side_projects.utils.find_high_gp_merge import FindHighGP
from side_projects.utils.line_notifier import LineNotifier


DEFAULT_URL = "https://forum.gamer.com.tw/C.php?bsn=23805&snA=729963&tnum=31"


def crawl_best_replies(url: str, headless: bool = True, mode: str = "2") -> list[str]:
    """爬取指定巴哈文章的爆文＋每一頁最高 GP 回覆，回傳字串 list。

    Args:
        url: 巴哈文章網址
        headless: 是否用無頭模式（排程時建議 True）
        mode: "1" 只抓第一筆爆文；"2" 抓全部爆文
    """
    driver_control = WebController(headless=headless)
    try:
        driver_control.get_url(url)
        finder = FindHighGP(driver_control.driver)

        all_best: list[str] = []
        all_best.extend(finder.scan_high_gp("content", mode))

        # 換頁邏輯跟 madhead_merge.py 一致
        while True:
            btns = driver_control.find_elements(By.CSS_SELECTOR, ".next")
            no_next = driver_control.find_elements(By.CSS_SELECTOR, ".next.no")
            if btns and not no_next:
                btns[0].click()
                time.sleep(5)
                all_best.extend(finder.scan_high_gp("content", mode))
            else:
                break
        return all_best
    finally:
        driver_control.close_windows()


def main() -> None:
    parser = argparse.ArgumentParser(description="巴哈爆文 → Claude 摘要 → LINE 推送")
    parser.add_argument("--url", default=DEFAULT_URL, help="巴哈文章網址")
    parser.add_argument("--headless", action="store_true", help="無頭模式（排程建議開啟）")
    parser.add_argument("--mode", default="2", choices=["1", "2"],
                        help="1=只抓第一筆爆文，2=全部爆文")
    parser.add_argument("--no-summarize", action="store_true", help="跳過 Claude 摘要")
    parser.add_argument("--no-line", action="store_true", help="只印結果，不推 LINE")
    args = parser.parse_args()

    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] 開始爬取：{args.url}")
    replies = crawl_best_replies(args.url, headless=args.headless, mode=args.mode)
    print(f"共取得 {len(replies)} 筆回覆")

    if not replies:
        print("沒有內容可推送，結束")
        return

    # 摘要步驟
    if args.no_summarize:
        message_body = "\n\n".join(replies)
    else:
        print("呼叫 Claude 產生摘要 ...")
        message_body = AISummarizer().summarize(replies)

    final = f"📢 巴哈爆文摘要（{datetime.now():%m/%d %H:%M}）\n\n{message_body}"
    print("=" * 40)
    print(final)
    print("=" * 40)

    # 推送步驟
    if args.no_line:
        print("(已跳過 LINE 推送)")
        return

    print("推送到 LINE ...")
    LineNotifier().send_text(final)
    print("✅ 已送達")


if __name__ == "__main__":
    main()

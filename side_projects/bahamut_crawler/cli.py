# Created: 2026-04-19
"""CLI 入口點。

設計原則：main() 越薄越好，只負責「解析參數 → 組裝元件 → 執行」。
商業邏輯都在 scraper.py 裡，這裡不寫 if/else 判斷流程。

使用方式：
    # 基本爬取
    python -m side_projects.bahamut_crawler.cli --bsn 23805 --sna 729963

    # 存進 SQLite + 顯示 DEBUG log
    python -m side_projects.bahamut_crawler.cli --bsn 23805 --sna 729963 --storage sqlite -v

    # 偵測到新爆文時發送 Discord 通知（需先設 DISCORD_WEBHOOK_URL 環境變數）
    export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/xxx/yyy"
    python -m side_projects.bahamut_crawler.cli --bsn 23805 --sna 729963 --notify discord

    # 用 LINE 通知（需先設 LINE_CHANNEL_ACCESS_TOKEN + LINE_USER_ID）
    export LINE_CHANNEL_ACCESS_TOKEN="..."
    export LINE_USER_ID="Uxxx..."
    python -m side_projects.bahamut_crawler --bsn 23805 --sna 729963 --notify line
"""
from __future__ import annotations

import argparse
import logging
import os
import sys

# 自動載入專案根目錄的 .env（裡面放 LINE token、Discord webhook 等敏感資訊）
# 若沒裝 python-dotenv 就跳過，不強制要求，保持向下相容
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .notifier import (
    ConsoleNotifier, DiscordNotifier, LINENotifier, NotificationTracker, Notifier,
)
from .scraper import BahamutScraper
from .storage import JSONStorage, SQLiteStorage, Storage


def setup_logging(verbose: bool) -> None:
    """設定 logging 輸出格式與等級。"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="巴哈姆特論壇文章爬蟲")
    parser.add_argument("--bsn", type=int, required=True, help="版號，如神魔之塔=23805")
    parser.add_argument("--sna", type=int, required=True, help="文章編號")
    parser.add_argument(
        "--storage",
        choices=["json", "sqlite"],
        default="json",
        help="儲存方式（預設 json）",
    )
    parser.add_argument(
        "--output",
        default="side_projects/output",
        help="輸出目錄或 SQLite 檔案路徑",
    )
    parser.add_argument(
        "--gp-threshold",
        type=int,
        default=15,
        help="只列出 GP 超過此門檻的回覆（預設 15）",
    )
    parser.add_argument(
        "--notify",
        choices=["none", "console", "discord", "line"],
        default="none",
        help="新爆文通知方式（console / discord / line）",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="顯示 DEBUG log")
    return parser.parse_args()


def build_storage(args: argparse.Namespace) -> Storage:
    """根據參數組裝 Storage（dependency injection 的入口）。"""
    if args.storage == "sqlite":
        return SQLiteStorage(f"{args.output}/bahamut.db")
    return JSONStorage(args.output)


def build_notifier(args: argparse.Namespace) -> Notifier | None:
    """根據參數組裝 Notifier。回傳 None 代表不通知。"""
    if args.notify == "console":
        return ConsoleNotifier()
    if args.notify == "discord":
        # 從環境變數讀，不要把 webhook 寫進 CLI flag，避免 shell history 外洩
        webhook = os.environ.get("DISCORD_WEBHOOK_URL")
        if not webhook:
            logging.error("請先設定環境變數 DISCORD_WEBHOOK_URL")
            sys.exit(2)
        return DiscordNotifier(webhook)
    if args.notify == "line":
        # LINENotifier 是 Adapter，底層會自動從 LINE_CHANNEL_ACCESS_TOKEN / LINE_USER_ID
        # 讀環境變數並驗證，我們不需要重複檢查
        try:
            return LINENotifier()
        except RuntimeError as e:
            logging.error(str(e))
            sys.exit(2)
    return None


def handle_notification(
    notifier: Notifier,
    post,
    gp_threshold: int,
    state_file: str,
) -> None:
    """比對爆文與 state file，只通知「沒通知過的新爆文」。"""
    tracker = NotificationTracker(state_file)
    candidates = [r for r in post.replies if r.gp > gp_threshold]
    new_ones = tracker.filter_new(post, candidates)

    if not new_ones:
        logging.info("沒有新爆文（已全部通知過），不發訊息")
        return

    notifier.notify(post, new_ones)
    tracker.mark_notified(post, new_ones)


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)

    storage = build_storage(args)
    notifier = build_notifier(args)

    try:
        with BahamutScraper() as scraper:
            post = scraper.crawl_post(args.bsn, args.sna)
            storage.save(post)

            # 印出高 GP 回覆摘要
            high_gp = post.high_gp_replies(threshold=args.gp_threshold)
            print(f"\n=== 共 {len(post.replies)} 則回覆，{len(high_gp)} 則超過 {args.gp_threshold} GP ===")
            for r in high_gp:
                marker = "[爆]" if r.is_exploded else f"[{r.gp}]"
                preview = r.content[:80].replace("\n", " ")
                print(f"{marker} B{r.floor} {r.author}: {preview}...")

            # 發通知（如果有指定 notifier）
            if notifier is not None:
                handle_notification(
                    notifier, post, args.gp_threshold,
                    state_file=f"{args.output}/notify_state.json",
                )

        return 0
    except Exception as e:
        logging.exception("Crawl failed: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())

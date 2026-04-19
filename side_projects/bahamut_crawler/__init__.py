# Created: 2026-04-19
"""巴哈姆特討論版爬蟲套件。

公開 API 只保留高層級物件，使用者不用關心內部實作細節。
"""
from .models import Post, Reply
from .notifier import ConsoleNotifier, DiscordNotifier, LINENotifier, Notifier
from .scraper import BahamutScraper

__all__ = [
    "Post", "Reply", "BahamutScraper",
    "Notifier", "ConsoleNotifier", "DiscordNotifier", "LINENotifier",
]
__version__ = "0.1.0"

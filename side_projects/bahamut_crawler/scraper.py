# Created: 2026-04-19
"""爬蟲核心（orchestration 層）。

職責：協調 Client 和 Parser，定義「怎麼爬一篇完整文章」的流程。
這一層才是商業邏輯，需求變動時只改這裡。
"""
from __future__ import annotations

import logging
from typing import Iterator

from .client import BahamutClient
from .models import Post, Reply
from .parser import BahamutParser

logger = logging.getLogger(__name__)


class BahamutScraper:
    """高層級 API，使用者只需要接觸這個類別。"""

    def __init__(
        self,
        client: BahamutClient | None = None,
        parser: BahamutParser | None = None,
    ):
        # 依賴注入（dependency injection）：測試時可以塞假的 client / parser
        self.client = client or BahamutClient()
        self.parser = parser or BahamutParser()

    def crawl_post(self, bsn: int, sn_a: int, max_pages: int = 50) -> Post:
        """爬完一篇文章的所有分頁，合併成一個 Post 物件。

        Args:
            bsn: 版號（神魔之塔 = 23805）
            sn_a: 文章編號
            max_pages: 保險上限，避免無窮迴圈

        Returns:
            Post 物件，其 replies 包含所有分頁的樓層
        """
        base_url = f"/C.php?bsn={bsn}&snA={sn_a}"
        all_replies: list[Reply] = []
        post: Post | None = None

        for page in range(1, max_pages + 1):
            url = f"{base_url}&page={page}"
            logger.info("Crawling page %d: %s", page, url)

            html = self.client.get(url)
            current_post = self.parser.parse_post(html, url, bsn, sn_a)

            # 第一頁拿來當主體（存標題、作者等 metadata）
            if post is None:
                post = current_post

            all_replies.extend(current_post.replies)

            # 檢查是否還有下一頁
            if not self.parser.has_next_page(html):
                logger.info("No more pages, stop at page %d", page)
                break

        assert post is not None, "至少要有第一頁"
        post.replies = all_replies
        return post

    def iter_high_gp_replies(
        self, bsn: int, sn_a: int, threshold: int = 15
    ) -> Iterator[Reply]:
        """以 generator 方式一筆一筆吐出高 GP 回覆。

        用 generator 的好處：記憶體友善，可搭配 for 迴圈即時處理。
        """
        post = self.crawl_post(bsn, sn_a)
        for reply in post.replies:
            if reply.gp > threshold:
                yield reply

    # 支援 with 語法，離開時自動關閉底層 HTTP session
    def __enter__(self) -> "BahamutScraper":
        return self

    def __exit__(self, *args) -> None:
        self.client.close()

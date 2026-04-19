# Created: 2026-04-19
"""HTML 解析層。

職責：把 HTML 字串變成 dataclass 物件。不碰網路、不碰儲存。

這層的好處：
    1. 純函式 → 給一份 HTML 永遠回同樣結果，超好測試
    2. 跟 HTTP 層解耦 → 拿瀏覽器存下來的 HTML 也能跑
    3. 網站改版只改這層 → 不影響其他程式
"""
from __future__ import annotations

import logging
from typing import Optional

from bs4 import BeautifulSoup

from .models import Post, Reply

logger = logging.getLogger(__name__)

EXPLODED_GP = 999999  # 爆文用這個數字代替「爆」，方便比大小與存 JSON


def _parse_gp(gp_text: str) -> int:
    """把 GP 文字（"25"、"爆"、"X1"、""）轉成整數。"""
    gp_text = gp_text.strip()
    if not gp_text:
        return 0
    if "爆" in gp_text:
        return EXPLODED_GP
    # 只留數字（去掉 X、噓、空白）
    digits = "".join(c for c in gp_text if c.isdigit())
    return int(digits) if digits else 0


class BahamutParser:
    """巴哈論壇頁面解析器。"""

    def parse_post(self, html: str, url: str, bsn: int, sn_a: int) -> Post:
        """解析一篇文章的完整頁面，回傳 Post 物件（含所有回覆）。"""
        soup = BeautifulSoup(html, "html.parser")

        title = self._extract_title(soup)
        author = self._extract_author(soup)
        replies = self._extract_replies(soup)

        return Post(
            url=url,
            title=title,
            author=author,
            bsn=bsn,
            sn_a=sn_a,
            replies=replies,
        )

    def _extract_title(self, soup: BeautifulSoup) -> str:
        node = soup.select_one(".c-post__header__title")
        return node.get_text(strip=True) if node else "(無標題)"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        node = soup.select_one(".username")
        return node.get_text(strip=True) if node else "(匿名)"

    def _extract_replies(self, soup: BeautifulSoup) -> list[Reply]:
        """抓出頁面上所有樓層。"""
        replies: list[Reply] = []

        for section in soup.select("section[id^='post_']"):
            reply = self._extract_single_reply(section)
            if reply is not None:
                replies.append(reply)

        return replies

    def _extract_single_reply(self, section) -> Optional[Reply]:
        """解析單一樓層。失敗就回 None，別讓整個爬蟲掛掉。"""
        try:
            floor_text = section.get("id", "post_0").replace("post_", "")
            floor = int(floor_text) if floor_text.isdigit() else 0

            author_node = section.select_one(".username")
            author = author_node.get_text(strip=True) if author_node else "(匿名)"

            gp_node = section.select_one(".postgp")
            gp = _parse_gp(gp_node.get_text() if gp_node else "")

            content_node = section.select_one(".c-article__content")
            content = content_node.get_text("\n", strip=True) if content_node else ""

            time_node = section.select_one(".edittime")
            posted_at = time_node.get("data-mtime") if time_node else None

            return Reply(
                floor=floor,
                author=author,
                gp=gp,
                content=content,
                posted_at=posted_at,
            )
        except Exception as e:
            logger.warning("Failed to parse reply section: %s", e)
            return None

    def has_next_page(self, html: str) -> bool:
        """判斷是否還有下一頁。"""
        soup = BeautifulSoup(html, "html.parser")
        # 有 .next 但沒有 .next.no，才是真的有下一頁
        return bool(soup.select(".next")) and not bool(soup.select(".next.no"))

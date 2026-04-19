# Created: 2026-04-19
"""HTTP 客戶端層。

職責：把 URL 變成 HTML 字串。只管「怎麼抓」，不管「抓什麼」。

進階技巧示範：
    1. requests.Session → 連線池、共用 headers、自動保存 cookie
    2. 重試機制（手寫版，不依賴 tenacity 讓你看懂原理）
    3. Rate limiting → 禮貌爬蟲，別把對方網站打爆
    4. User-Agent rotation → 避免被認出是爬蟲
    5. logging 取代 print → 可控制輸出等級，production ready
"""
from __future__ import annotations

import logging
import random
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)


# 一般網站都會檢查 User-Agent，隨機輪替避免被認出同一個爬蟲
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]


class BahamutClient:
    """巴哈論壇專用 HTTP 客戶端。"""

    BASE_URL = "https://forum.gamer.com.tw"

    def __init__(
        self,
        timeout: int = 10,
        max_retries: int = 3,
        rate_limit: float = 1.0,  # 每次請求間隔至少幾秒
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self._last_request_at: float = 0.0

        # Session 的好處：連線池、共用 cookies、共用 headers
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "zh-TW,zh;q=0.9",
        })

    def _respect_rate_limit(self) -> None:
        """確保兩次請求之間有足夠的間隔（禮貌爬蟲）。"""
        elapsed = time.time() - self._last_request_at
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request_at = time.time()

    def get(self, url: str, params: Optional[dict] = None) -> str:
        """發出 GET 請求，回傳 HTML 字串。失敗會自動重試。

        Args:
            url: 目標網址（可以是完整 URL 或相對路徑）
            params: URL query string 參數

        Raises:
            requests.RequestException: 重試 max_retries 次後仍失敗
        """
        # 支援傳入相對路徑（例如 "/C.php?bsn=..."）
        if url.startswith("/"):
            url = f"{self.BASE_URL}{url}"

        # 指數退避（exponential backoff）：失敗後越等越久，避免雪崩
        for attempt in range(1, self.max_retries + 1):
            self._respect_rate_limit()
            try:
                logger.debug("GET %s (attempt %d)", url, attempt)
                resp = self.session.get(url, params=params, timeout=self.timeout)
                resp.raise_for_status()  # 4xx/5xx 直接拋例外
                return resp.text
            except requests.RequestException as e:
                wait = 2 ** attempt  # 2, 4, 8 秒
                logger.warning(
                    "Request failed (%s), retry in %ds. [%d/%d]",
                    e, wait, attempt, self.max_retries,
                )
                if attempt == self.max_retries:
                    raise
                time.sleep(wait)

        raise RuntimeError("unreachable")  # 不會執行到，但讓 type checker 開心

    def close(self) -> None:
        """關閉 Session，釋放連線。"""
        self.session.close()

    # 讓 BahamutClient 可以用 with 語法
    def __enter__(self) -> "BahamutClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

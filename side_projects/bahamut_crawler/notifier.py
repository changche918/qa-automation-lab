# Created: 2026-04-19
"""通知層。

職責：把「有新爆文」這件事送到使用者的裝置。
用 ABC 定義介面，Discord / Telegram / Slack 都只要實作 notify() 即可。

使用情境：
    - 排程每小時爬一次，一有新爆文立刻 push 到手機
    - 可搭配 GitHub Actions + cron 做成零成本的監控服務
"""
from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

import requests

from .models import Post, Reply

logger = logging.getLogger(__name__)


class Notifier(ABC):
    """通知介面。所有通知方式都實作這個介面。"""

    @abstractmethod
    def notify(self, post: Post, new_replies: list[Reply]) -> None:
        ...


class ConsoleNotifier(Notifier):
    """印到 terminal，用於開發測試。避免真的發訊息把自己砲炸。"""

    def notify(self, post: Post, new_replies: list[Reply]) -> None:
        print(f"\n🔔 [Console] {post.title} 有 {len(new_replies)} 則新爆文")
        for r in new_replies:
            print(f"   B{r.floor} {r.author}: {r.content[:60]}...")


class DiscordNotifier(Notifier):
    """透過 Discord Webhook 發訊息。

    設定步驟：
        1. Discord 頻道 → 編輯頻道 → 整合 → Webhook → 新增 Webhook
        2. 複製 Webhook URL（長這樣：https://discord.com/api/webhooks/xxx/yyy）
        3. 設成環境變數：export DISCORD_WEBHOOK_URL="https://..."

    安全性：Webhook URL 等同於密碼，千萬不要 commit 進 git。
    """

    def __init__(self, webhook_url: str, timeout: int = 10):
        if not webhook_url:
            raise ValueError("Discord webhook URL 不能為空")
        self.webhook_url = webhook_url
        self.timeout = timeout

    def notify(self, post: Post, new_replies: list[Reply]) -> None:
        if not new_replies:
            return  # 沒有新爆文就不發，避免騷擾

        # Discord Embed 是結構化訊息，看起來比純文字專業
        embeds = [self._build_embed(post, r) for r in new_replies[:10]]  # 最多 10 則/次

        payload = {
            "username": "巴哈爆文通知",
            "content": f"🔥 **{post.title}** 發現 {len(new_replies)} 則新爆文",
            "embeds": embeds,
        }

        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            logger.info("Discord 通知送出：%d 則爆文", len(new_replies))
        except requests.RequestException as e:
            # 通知失敗不該讓整個爬蟲爆炸，記 log 就好
            logger.error("Discord 通知失敗：%s", e)

    def _build_embed(self, post: Post, reply: Reply) -> dict:
        """組出單一筆爆文的 Discord Embed。"""
        preview = reply.content[:300] + ("..." if len(reply.content) > 300 else "")
        return {
            "title": f"B{reply.floor} by {reply.author}",
            "description": preview,
            "url": post.url,
            "color": 0xFF6B00,  # 橘色代表「爆」
            "fields": [
                {"name": "GP", "value": "爆" if reply.is_exploded else str(reply.gp), "inline": True},
                {"name": "發文時間", "value": reply.posted_at or "不明", "inline": True},
            ],
        }


class LINENotifier(Notifier):
    """Adapter：把 side_projects/utils/line_notifier.py 的 LineNotifier
    包裝成符合 Notifier 介面的物件。

    這就是 Adapter Pattern 的經典應用：
        - 舊版 LineNotifier 只會 send_text(str) → 不符 Notifier 介面
        - 我們不改舊版（OCP 原則），寫一個薄轉接層
        - 爬蟲 code 用 Notifier 抽象介面，不知道底下是誰實作

    需要的環境變數（由底層 LineNotifier 讀取）：
        LINE_CHANNEL_ACCESS_TOKEN
        LINE_USER_ID
    """

    def __init__(
        self,
        channel_access_token: str | None = None,
        user_id: str | None = None,
    ):
        # 延遲 import：避免 side_projects.utils 不可用時整個 package 掛掉
        from side_projects.utils.line_notifier import LineNotifier as _LineImpl

        self._impl = _LineImpl(
            channel_access_token=channel_access_token,
            user_id=user_id,
        )

    def notify(self, post: Post, new_replies: list[Reply]) -> None:
        if not new_replies:
            return

        text = self._format_message(post, new_replies)
        try:
            self._impl.send_text(text)
            logger.info("LINE 通知送出：%d 則爆文", len(new_replies))
        except Exception as e:
            # 通知失敗不該讓整個爬蟲爆炸
            logger.error("LINE 通知失敗：%s", e)

    def _format_message(self, post: Post, new_replies: list[Reply]) -> str:
        """組出純文字訊息。LINE 單則最多 5000 字，底層會自動截斷。"""
        lines = [
            f"🔥 {post.title}",
            f"發現 {len(new_replies)} 則新爆文：",
            "",
        ]
        for r in new_replies[:5]:  # 只列前 5 則，避免訊息太長
            preview = r.content[:80].replace("\n", " ")
            gp_label = "爆" if r.is_exploded else str(r.gp)
            lines.append(f"[{gp_label}] B{r.floor} {r.author}")
            lines.append(f"  {preview}...")
            lines.append("")

        if len(new_replies) > 5:
            lines.append(f"...還有 {len(new_replies) - 5} 則未列出")

        lines.append(f"\n原文：{post.url}")
        return "\n".join(lines)


class NotificationTracker:
    """記住「已通知過哪些樓層」，避免重複發通知。

    實作方式：用一個 JSON 檔當 state store。
    之後要升級成 Redis / SQLite 只改這個類別即可。
    """

    def __init__(self, state_file: str | Path):
        self.state_file = Path(state_file)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self._state = self._load()

    def _load(self) -> dict[str, list[int]]:
        if not self.state_file.exists():
            return {}
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self) -> None:
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def _key(self, post: Post) -> str:
        return f"bsn{post.bsn}_snA{post.sn_a}"

    def filter_new(self, post: Post, candidates: list[Reply]) -> list[Reply]:
        """從候選清單中過濾出「還沒通知過」的樓層。"""
        notified_floors = set(self._state.get(self._key(post), []))
        return [r for r in candidates if r.floor not in notified_floors]

    def mark_notified(self, post: Post, replies: list[Reply]) -> None:
        """標記這些樓層已通知。"""
        key = self._key(post)
        existing = set(self._state.get(key, []))
        existing.update(r.floor for r in replies)
        self._state[key] = sorted(existing)
        self._save()

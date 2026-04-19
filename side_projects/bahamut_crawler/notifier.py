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
    """透過 LINE Messaging API 發訊息。

    ⚠️ 注意：LINE Notify 已於 2025-04-01 停止服務，本類別使用新的 Messaging API。

    設定步驟：
        1. 到 https://developers.line.biz/console/ 登入並建立 Provider
        2. 建立 "Messaging API" channel
        3. 到 Basic settings → 取得 Channel secret
        4. 到 Messaging API → Issue 一組 Channel access token
        5. 手機開啟 LINE，掃 QR code 加 bot 為好友
        6. 到 Messaging API 頁面底部 → 取得 Your user ID
        7. 設定環境變數：
               export LINE_CHANNEL_TOKEN="xxx"
               export LINE_USER_ID="Uxxx..."   (或用 broadcast 發給所有好友)

    費用：免費方案每月 200 則 push message；broadcast 不計數。
    """

    PUSH_URL = "https://api.line.me/v2/bot/message/push"
    BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"

    def __init__(
        self,
        channel_token: str,
        user_id: str | None = None,  # None = broadcast 給所有加過好友的人
        timeout: int = 10,
    ):
        if not channel_token:
            raise ValueError("LINE channel token 不能為空")
        self.channel_token = channel_token
        self.user_id = user_id
        self.timeout = timeout

    def notify(self, post: Post, new_replies: list[Reply]) -> None:
        if not new_replies:
            return

        # LINE 一則 push 最多 5 個 message 物件，所以截斷
        messages = [self._build_header_message(post, len(new_replies))]
        for r in new_replies[:4]:
            messages.append(self._build_reply_message(post, r))

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.channel_token}",
        }

        # 有指定 user_id 用 push（點對點），否則用 broadcast（全部好友）
        if self.user_id:
            url = self.PUSH_URL
            payload = {"to": self.user_id, "messages": messages}
        else:
            url = self.BROADCAST_URL
            payload = {"messages": messages}

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            logger.info("LINE 通知送出：%d 則爆文", len(new_replies))
        except requests.RequestException as e:
            # LINE 回 400 通常是訊息格式錯；回 401 是 token 錯；回 429 是額度用完
            logger.error("LINE 通知失敗：%s (response: %s)",
                         e, getattr(e.response, "text", "N/A"))

    def _build_header_message(self, post: Post, count: int) -> dict:
        return {
            "type": "text",
            "text": f"🔥 {post.title}\n發現 {count} 則新爆文！\n{post.url}",
        }

    def _build_reply_message(self, post: Post, reply: Reply) -> dict:
        """用 Flex Message 讓訊息有樣式（進階寫法，展示能力）。"""
        preview = reply.content[:200] + ("..." if len(reply.content) > 200 else "")
        gp_label = "爆" if reply.is_exploded else str(reply.gp)
        return {
            "type": "text",
            "text": f"[{gp_label}] B{reply.floor} {reply.author}\n{preview}",
        }


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

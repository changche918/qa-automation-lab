# Created: 2026-04-16
"""使用 LINE Messaging API 推送訊息到你的 LINE。

前置準備：
    1. 到 https://developers.line.biz/console/ 建立一個 Provider
    2. 在 Provider 底下新增 Messaging API channel
    3. 在 channel 的 Basic settings 取得「Channel Access Token (long-lived)」
    4. 用你的 LINE 加這個 bot 為好友
    5. 拿到你自己的 userId（兩種方法）：
       a) 到 channel 的 Webhook settings 暫時開啟 webhook + 傳訊給 bot，
          從 webhook log 看 event.source.userId
       b) 用 LIFF / Login API 取得
    6. 將 token 與 userId 放進環境變數：
          LINE_CHANNEL_ACCESS_TOKEN
          LINE_USER_ID
簡易流程：
    你的 Python 程式
      ↓ 透過 requests.post 發出 HTTP 請求
      ↓ （帶著 token 證明你是合法使用者）
      ↓
    LINE 官方伺服器 (api.line.me)
        ↓ 驗證 token、找到 user_id
        ↓
    你的手機 LINE App ← 收到訊息
"""
import os

import requests

class LineNotifier:
    PUSH_URL = "https://api.line.me/v2/bot/message/push"
    MAX_TEXT_LEN = 4900  # LINE 單則文字上限 5000 字，保留一點 buffer

    def __init__(
        self,
        channel_access_token: str | None = None,
        user_id: str | None = None,
    ):
        self.token = channel_access_token or os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
        self.user_id = user_id or os.environ.get("LINE_USER_ID")
        if not self.token or not self.user_id:
            raise RuntimeError(
                "缺少 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_USER_ID，請確認環境變數已設定"
            )

    def send_text(self, text: str) -> dict:
        """推送一則文字訊息到指定使用者。"""
        if len(text) > self.MAX_TEXT_LEN:
            text = text[: self.MAX_TEXT_LEN] + "\n...(訊息過長已截斷)"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        body = {
            "to": self.user_id,
            "messages": [{"type": "text", "text": text}],
        }
        resp = requests.post(self.PUSH_URL, headers=headers, json=body, timeout=30)
        resp.raise_for_status()
        return resp.json()

# Created: 2026-04-16
"""呼叫 Claude API 把爬到的巴哈回覆文內容做摘要。

使用方式：
    from side_projects.utils.ai_summarizer import AISummarizer
    summary = AISummarizer().summarize(["[爆] 內文1...", "[30] 內文2..."])

需要環境變數：
    ANTHROPIC_API_KEY   （到 https://console.anthropic.com/ 申請）
"""
import os

from anthropic import Anthropic


class AISummarizer:
    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-6"):
        # 金鑰優先使用參數傳入，其次讀環境變數
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def summarize(self, texts: list[str], max_tokens: int = 1024) -> str:
        """把多則回覆文合併後，請 Claude 用繁中整理成短摘要。"""
        if not texts:
            return "（今天沒有抓到爆文或高 GP 回覆）"

        joined = "\n\n---\n\n".join(texts)
        prompt = (
            "以下是巴哈姆特論壇上的爆文或高 GP 回覆，請你幫我用繁體中文整理成簡潔摘要，\n"
            "讓我在手機上看 LINE 時能快速掌握內容。\n\n"
            "輸出格式：\n"
            "  1. 每一篇用 1~2 句話概括重點，前面標上原本的 [爆] 或 [GP數]\n"
            "  2. 最後一行給一個整體氛圍判斷（熱烈討論／爭論／正面／負面／閒聊）\n\n"
            "原始內容：\n"
            f"{joined}"
        )

        msg = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text

# Created: 2026-04-19
"""資料模型層。

使用 dataclass 定義「爬到的資料長什麼樣」。
好處：
    1. 型別註解 → IDE 自動補全、減少 bug
    2. 自動產生 __init__、__repr__、__eq__
    3. 比 dict 清楚 (post.title vs post["title"])
    4. 面試時能證明你會用現代 Python
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Reply:
    """單一樓層的回覆。"""
    floor: int                  # 樓層編號（B1, B2, ...）
    author: str                 # 作者 ID
    gp: int                     # GP 數（爆文用 float("inf") 或直接定義常數 999999）
    content: str                # 內文純文字
    posted_at: Optional[str] = None  # 發文時間（原始字串，如 "2026-04-19 10:30"）

    @property
    def is_exploded(self) -> bool:
        """是否為爆文。"""
        return self.gp >= 100


@dataclass
class Post:
    """一篇文章（含其所有回覆）。"""
    url: str
    title: str
    author: str
    bsn: int                    # 版號
    sn_a: int                   # 文章編號
    replies: list[Reply] = field(default_factory=list)
    crawled_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def best_reply(self) -> Optional[Reply]:
        """回傳這篇文中 GP 最高的回覆。"""
        return max(self.replies, key=lambda r: r.gp, default=None)

    def high_gp_replies(self, threshold: int = 15) -> list[Reply]:
        """回傳 GP 超過門檻的所有回覆。"""
        return [r for r in self.replies if r.gp > threshold]

    def to_dict(self) -> dict:
        """轉成 dict，方便存 JSON。"""
        return asdict(self)

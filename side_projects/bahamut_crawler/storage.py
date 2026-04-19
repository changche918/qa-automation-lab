# Created: 2026-04-19
"""儲存層。

職責：把 Post 物件存到某個地方。
用 abstract base class 定義介面，之後要換 SQLite / MongoDB / S3 都只改這裡。
"""
from __future__ import annotations

import json
import logging
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path

from .models import Post

logger = logging.getLogger(__name__)


class Storage(ABC):
    """儲存介面。所有儲存方式都實作這個介面。"""

    @abstractmethod
    def save(self, post: Post) -> None:
        ...


class JSONStorage(Storage):
    """存成 JSON 檔（每篇一個檔）。適合小量資料、快速查看。"""

    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, post: Post) -> None:
        filename = f"bsn{post.bsn}_snA{post.sn_a}.json"
        path = self.output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(post.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Saved to %s", path)


class SQLiteStorage(Storage):
    """存進 SQLite。適合要做查詢、統計的情境。"""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    bsn INTEGER, sn_a INTEGER,
                    url TEXT, title TEXT, author TEXT, crawled_at TEXT,
                    UNIQUE(bsn, sn_a)
                );
                CREATE TABLE IF NOT EXISTS replies (
                    id INTEGER PRIMARY KEY,
                    post_id INTEGER,
                    floor INTEGER, author TEXT, gp INTEGER, content TEXT,
                    posted_at TEXT,
                    FOREIGN KEY(post_id) REFERENCES posts(id)
                );
            """)

    def save(self, post: Post) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            # UPSERT：同一篇重跑時更新而非重複插入
            cur.execute("""
                INSERT INTO posts (bsn, sn_a, url, title, author, crawled_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(bsn, sn_a) DO UPDATE SET
                    url=excluded.url, title=excluded.title,
                    author=excluded.author, crawled_at=excluded.crawled_at
                RETURNING id
            """, (post.bsn, post.sn_a, post.url, post.title, post.author, post.crawled_at))
            post_id = cur.fetchone()[0]

            # 重新寫入所有回覆（簡化處理；正式應用可做 diff）
            cur.execute("DELETE FROM replies WHERE post_id = ?", (post_id,))
            cur.executemany("""
                INSERT INTO replies (post_id, floor, author, gp, content, posted_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (post_id, r.floor, r.author, r.gp, r.content, r.posted_at)
                for r in post.replies
            ])
        logger.info("Saved post %d to SQLite (%d replies)", post.sn_a, len(post.replies))

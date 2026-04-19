# Created: 2026-04-19
"""Package 的直接執行入口。

有了這個檔，就可以用 `python -m side_projects.bahamut_crawler` 執行，
不用打完整的 `.cli` 子模組路徑。

標準庫也是這樣設計的，例如：
    python -m http.server    → 背後就是 http/server.py 裡面有 __main__.py 機制
    python -m json.tool
    python -m pip install ...
"""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

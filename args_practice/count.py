import argparse

# 設定 argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', action='count', default=0)
args = parser.parse_args()

# levels 對應 -v 的數量
levels = ["WARNING", "INFO", "DEBUG"] # 0 1 2
level = levels[min(args.v, len(levels) - 1)]
print(f"目前等級：{level}（打了 {args.v} 個 -v）")

"""
args.v = 1
         ↓
min(1, 2) = 1
         ↓
levels[1] = "INFO"
         ↓
level = "INFO"
"""

# 模擬不同等級的訊息
messages = [
    ("WARNING", "這是 WARNING"),
    ("INFO",    "這是 INFO"),
    ("DEBUG",   "這是 DEBUG"),
]

for msg_level, msg in messages:
    if levels.index(msg_level) <= levels.index(level):
        print(msg)

        
"""執行方式
# 預設只看 WARNING
$ python args_practice/count.py
WARNING: 這是 WARNING

# -v 看到 INFO
$ python args_practice/count.py -v
WARNING: 這是 WARNING
INFO: 這是 INFO

# -vv 全看
$ python args_practice/count.py -vv
WARNING: 這是 WARNING
INFO: 這是 INFO
DEBUG: 這是 DEBUG
"""
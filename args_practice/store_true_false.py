import argparse

"""
store_true  → 「按下去才會亮」，預設是暗的（False）
store_false → 「按下去才會暗」，預設是亮的（True）
"""

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true")
parser.add_argument("--visible", action="store_false")

args = parser.parse_args()  # 解析 terminal 輸入的參數
print(args)                 # 印出整個 Namespace

# python main.py --headless
# → args.headless = True

# python main.py --visible
# → args.visible = False

# python main.py  # 都不打
# → args.headless = False（store_true 預設是 False）
# → args.visible  = True （store_false 預設是 True）
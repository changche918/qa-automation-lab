import argparse

# 20260405 請 AI 提供範例
parser = argparse.ArgumentParser()
parser.add_argument("--v", action="count", default=0)

args = parser.parse_args()  # 解析 terminal 輸入的參數
print(args)                 # 印出整個 Namespace

# python main.py --v        # → args.v = 1
# python main.py --v --v    # → args.v = 2
# python main.py --v --v --v # → args.v = 3
# 常用在控制 log 詳細程度 (20260405 為啥要這樣用? 範例是?)
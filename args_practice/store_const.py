import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode", action="store_const", const=42)

args = parser.parse_args()  # 解析 terminal 輸入的參數
print(args)                 # 印出整個 Namespace

# python main.py --mode
# # → args.mode = 42  固定存你指定的值

# python main.py  # 不打
# # → args.mode = None
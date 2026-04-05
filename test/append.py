import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--url", action="append")

args = parser.parse_args()  # 解析 terminal 輸入的參數
print(args)                 # 印出整個 Namespace

# python main.py --url abc.com --url def.com
# # → args.url = ["abc.com", "def.com"]  每次出現都加進 list
import argparse

# 20260405 store 會不會有預設值的問題
parser = argparse.ArgumentParser()
parser.add_argument("--name", action="store")

args = parser.parse_args()  # 解析 terminal 輸入的參數
print(args)                 # 印出整個 Namespace
print(args.name)            # 印出單一參數

# python main.py --name John 或是 python main.py --name John,Amy,Ryan
# → args.name = "John"  輸入什麼存什麼
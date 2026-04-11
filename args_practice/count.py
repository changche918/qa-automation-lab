import argparse

# 設定 argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', action='count', default=0)
args = parser.parse_args()

print(args)

if args.v >= 1:
    print("基本資訊")
if args.v >= 2:
    print("詳細資訊")
if args.v >= 3:
    print("除錯資訊，全部印出來")

        
"""執行方式
$ python args_practice/count.py -v
"""

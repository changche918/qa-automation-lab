import argparse

# 設定 argparse
parser = argparse.ArgumentParser()
# parser.add_argument('-v', action='count', default=0)
parser.add_argument('-vv', default='xxxx')
args = parser.parse_args()

print(args)
20260411
-v -vv >>> 為什麼-v -v 可以 -vvvv 也可以，會不會衝突

# if args.v >= 1:
#     print("基本資訊")
# if args.v >= 2:
#     print("詳細資訊")
# if args.v >= 3:
#     print("除錯資訊，全部印出來")

        
"""執行方式
$ python args_practice/count.py -v
"""

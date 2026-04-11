import argparse

parser = argparse.ArgumentParser()
 # 有 dest 就聽 dest 的，沒有就把 -- 去掉當名字。只有一個名字能用，append 就是存到陣列
parser.add_argument('--host', action='append', dest='hosts')

parser.add_argument('--env', default='production') # 使用者沒給值，預設就 prod
args = parser.parse_args() # parse_args() 就是把命令列的字串，解析成 Python 可以用的物件

print(args)
print(f"部署環境：{args.env}")

for h in args.hosts:
    print(f"  → 部署到 {h}")

"""執行方式
# 同時部署到三台主機
$ python args_practice/append.py  --host 10.0.0.1  --host 10.0.0.2  --host 10.0.0.3

部屬到 lab 就是 python args_practice/append.py --env=lab 或是 --env lab 也可以
部署環境：production，
  → 部署到 10.0.0.1
  → 部署到 10.0.0.2
  → 部署到 10.0.0.3
"""
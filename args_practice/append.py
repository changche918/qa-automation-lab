import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', action='append', dest='hosts')
parser.add_argument('--env', default='production')
args = parser.parse_args()

print(f"部署環境：{args.env}")
for h in args.hosts:
    print(f"  → 部署到 {h}")

"""執行方式
# 同時部署到三台主機
$ python args_practice/append.py  --host 10.0.0.1  --host 10.0.0.2  --host 10.0.0.3

部署環境：production
  → 部署到 10.0.0.1
  → 部署到 10.0.0.2
  → 部署到 10.0.0.3
"""
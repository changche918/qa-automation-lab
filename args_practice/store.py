import argparse

parser = argparse.ArgumentParser()
# parser.add_argument('--host', default='127.0.0.1')
# parser.add_argument('--port', type=int, default=8080)
# parser.add_argument('--workers', type=int, default=4)
args = parser.parse_args()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=8080)
parser.add_argument('--workers', type=int, default=4)

print(f"啟動伺服器 {args.host}:{args.port}")
print(f"Worker 數量：{args.workers}")


"""執行方式
# 用預設值啟動
$ python args_practice\store.py
啟動伺服器 127.0.0.1:8080
Worker 數量：4

# 自訂 port 與 worker
$ python args_practice\store.py --host 0.0.0.0 --port 3000 --workers 8
啟動伺服器 0.0.0.0:3000
Worker 數量：8
"""
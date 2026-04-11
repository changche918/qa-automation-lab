import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1') # 使用者給值 > store 負責存，沒給值，拿 default 的值
parser.add_argument('--port', type=int, default=8080)
args = parser.parse_args()

print(f"伺服器：{args.host}:{args.port}")


"""執行方式
$ python args_practice\store.py
"""
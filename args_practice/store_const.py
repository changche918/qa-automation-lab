import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group() # 可以看一下 default 值是什麼意思 dest,action,const 的意思
group.add_argument('--json', dest='fmt',
                   action='store_const', const='json')
group.add_argument('--csv', dest='fmt',
                   action='store_const', const='csv')
parser.set_defaults(fmt='json')
args = parser.parse_args()

print(f"匯出格式：{args.fmt}")


"""執行方式
# 預設 json
$ python args_practice/store_const.py
匯出格式：json

# 指定 csv
$  python args_practice/store_const.py --csv
匯出格式：csv

# 兩個不能同時用（互斥）
$ python export.py --json --csv
error: argument --csv: not allowed with argument --json
"""
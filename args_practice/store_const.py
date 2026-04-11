import argparse

parser = argparse.ArgumentParser()
size = parser.add_mutually_exclusive_group() # parser.add_mutually_exclusive_group() 就是在解析器裡建立一個「只能選一個」的群組
size.add_argument('--large', dest='size', action='store_const', const='大杯')
size.add_argument('--small', dest='size', action='store_const', const='小杯')
parser.set_defaults(size='中杯') # 也是可以寫成 size.add_argument('--small', dest='size', action='store_const', const='小杯', default='中杯')

args = parser.parse_args()
print(f"你點的是：{args.size}")

"""執行方式
$ python args_practice/store_const.py --small
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--no-save', dest='save', action='store_false')
args = parser.parse_args()

if args.save:
    print("儲存檔案")
else:
    print("不儲存")


"""執行方式
$ python args_practice/store_false.py --no-save
"""
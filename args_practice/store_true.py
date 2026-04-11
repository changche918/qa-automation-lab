import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

print(args)
if args.verbose:
    print(f"開始下載：{args.url}")

if args.verbose:
    print("下載完成")

"""執行方式
$ python args_practice/store_true.py --url https://example.com/file.zip -v
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True)
parser.add_argument('--v', action='store_true')
args = parser.parse_args()

# 因為在第一步定義了 --verbose，argparse 會自動把橫線拿掉，變成 args 物件的一個屬性。
if args.v:
    print(f"開始下載：{args.url}")

# 模擬下載
if args.v:
    print("下載完成")

"""執行方式
# 靜默模式（不印任何東西）
$ python args_practice/store_true.py --url https://example.com/file.zip

# 詳細模式
$ python args_practice/store_true.py  --url https://example.com/file.zip --verbose
開始下載：https://example.com/file.zip
下載完成
"""
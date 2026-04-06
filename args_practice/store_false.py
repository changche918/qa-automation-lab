import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, default=10)
parser.add_argument('--no-save', dest='save', action='store_false')
args = parser.parse_args()

for epoch in range(args.epochs):
    print(f"訓練 epoch {epoch+1}")

if args.save:
    print("儲存模型...")
else:
    print("略過儲存（測試模式）")


"""執行方式
# 正常訓練（會儲存）
$ python args_practice/store_false.py --epochs 3
訓練 epoch 1 / 2 / 3
儲存模型...

# 測試時不想存檔
$ python args_practice/store_false.py --epochs 3 --no-save
訓練 epoch 1 / 2 / 3
略過儲存（測試模式）
"""
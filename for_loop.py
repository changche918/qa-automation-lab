# ========================================
# 5. FOR LOOP - 迴圈
# ========================================
# 基本用法:
#   for item in iterable: ...  (遍歷可迭代對象)
#   for i in range(start, stop, step): ... (遍歷數字範圍)
#   while condition: ... (條件迴圈)
# - range(n): 生成 0 到 n-1 的數字
# - range(start, stop): 生成 start 到 stop-1 的數字
# - range(start, stop, step): 指定步長
# - break: 跳出迴圈
# - continue: 跳過當前迭代，進入下一次

print("5. FOR LOOP 迴圈")

# for...in 迴圈
colors = ["red", "green", "blue"]
for color in colors:
    print(f"顏色: {color}")

# for...range() 迴圈
for i in range(5):           # 0, 1, 2, 3, 4
    print(f"i = {i}")
print("----")
for i in range(1, 5):        # 1, 2, 3, 4 (不包括5)
    print(f"i = {i}")
print("----")
for i in range(0, 10, 2):    # 步長為2
    print(f"i = {i}")
print("----")
# enumerate - 獲取索引和值
# enumerate() 是一個內置函數，可以同時獲取索引和元素值
# 語法: enumerate(iterable, start=0)
# - iterable: 可迭代對象 (列表、字符串、元組等)
# - start: 起始索引（默認為0）
print("\nEnumerate 基本用法:")
for index, color in enumerate(colors):
    print(f"{index}: {color}")

# enumerate 與手動追蹤索引的對比
# print("\n手動方式 vs enumerate:")
# print("手動方式:")

# for i in range(len(colors)):
#     print(f"{i}: {colors[i]}")

# print("Enumerate方式 (更簡潔):")
# for i, color in enumerate(colors):
#     print(f"{i}: {color}")

# # enumerate 可以指定起始索引
# print("\nEnumerate 自定義起始索引 (start=1):")
# for index, color in enumerate(colors, start=1):
#     print(f"{index}: {color}")

# # TODO:自己看 - 實用例子：處理購物清單
# print("\nEnumerate 實用例子 - 購物清單:")
# shopping_list = ["牛奶", "麵包", "雞蛋", "蔬菜"]
# for num, item in enumerate(shopping_list, start=1):
#     print(f"第{num}項: {item}")

# WHILE 迴圈
print("\nWhile 迴圈:")
count = 0
while count < 3:
    print(f"count = {count}")
    count += 1

# break 和 continue
print("\nBreak 和 Continue:")
for i in range(10):
    if i == 3:
        continue  # 跳過
    if i == 7:
        break     # 停止迴圈
    print(i)
# ========================================
# 進階案例 1: 九九乘法表 (巢狀 for 迴圈)
# ========================================
print("\n--- 進階案例 1: 九九乘法表 ---")
# TODO: 嘗試用不同的方式輸出乘法表（例如只輸出對角線、或倒序）- 有空再玩
for i in range(1, 10):
    row = ""
    for j in range(1, 10):
        row += f"{i*j:3d} "  # :3d 表示3位數字右對齊
    print(row)

# ========================================
# 進階案例 2: 猜數字遊戲 (使用 while + break)
# ========================================
print("\n--- 進階案例 2: 猜數字遊戲 ---")
# TODO: 添加試次限制、難度級別選擇、分數計算等功能 - 有空再玩
# import random

# secret_number = random.randint(1, 100)
# attempt_count = 0
# max_attempts = 10

# print(f"我想了一個1到100之間的數字，你有{max_attempts}次機會猜對它！")
# print("提示: 輸入 'quit' 可以放棄\n")

# while True:
#     try:
#         user_input = input(f"第 {attempt_count + 1} 次: 請輸入你的猜測 (1-100): ").strip()
        
#         # 檢查是否要放棄
#         if user_input.lower() == 'quit':
#             print(f"放棄了。正確答案是 {secret_number}")
#             break
        
#         # 轉換為整數
#         guess = int(user_input)
        
#         # 驗證輸入範圍
#         if guess < 1 or guess > 100:
#             print("❌ 請輸入1到100之間的數字")
#             continue
        
#         attempt_count += 1
        
#         # 比較
#         if guess == secret_number:
#             print(f"🎉 恭喜！你在第 {attempt_count} 次成功猜對了！")
#             # 計算分數 (嘗試次數越少分數越高)
#             score = max(0, 100 - (attempt_count - 1) * 10)
#             print(f"⭐ 你的分數: {score} 分")
#             break
#         elif guess < secret_number:
#             remaining = max_attempts - attempt_count
#             print(f"💡 太小了！還有 {remaining} 次機會")
#         else:
#             remaining = max_attempts - attempt_count
#             print(f"💡 太大了！還有 {remaining} 次機會")
        
#         # 檢查是否超過最大嘗試次數
#         if attempt_count >= max_attempts:
#             print(f"❌ 遊戲結束！你已經用完所有 {max_attempts} 次機會")
#             print(f"正確答案是 {secret_number}")
#             break
            
#     except ValueError:
#         print("❌ 請輸入有效的數字")
#         continue


"""
TODO: 
1. 參考L80 寫出 3層巢狀迴圈 各跑20次, 
    1. 印出 i, j, k 的值
    2. 當i=5, j=5, k=5 時印出 "找到目標!" 並跳出所有迴圈
    hint: for i in range():
2. 寫一個"簡單的猜數字遊戲" (只要能玩就好, 怎樣都行)
    hint: 使用 while 迴圈, break, 使用input() 取得使用者輸入
"""

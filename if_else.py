# ========================================
# 4. IF ELSE - 條件判斷
# ========================================
# 基本用法: if condition: ... elif condition: ... else: ...
# - if: 如果條件為真，執行代碼
# - elif: 其他條件為真，執行代碼 (可以有多個)
# - else: 上述都不符合時執行
# - 邏輯運算符: and, or, not
# - 比較運算符: ==, !=, <, >, <=, >=, in, not in
# not 運算符: 反轉布林值
print("4. IF ELSE 條件判斷")
age = 5

def age_reduce(x):
    if x < 15:
        print("增加3歲")
        return x + 3
    else:
        print("減少3歲")
        return x - 3

if age < 13:
    print("你是小孩")
    if age_reduce(age) < 10:
    # if age < 10:
        print("還在念小學")
    else:
        print("已經上中學了")
        if age == 12:
            print("你12歲")
elif age < 18:
    print("你是青少年")
    if age_reduce(age) < 15:
        print("還在念中學")
elif age < 65:
    print("你是成人")
else:
    print("你是長者")

# 三元運算符 (ternary operator)
status = "成人" if age >= 18 else "未成年"
print(f"身份: {status}")

# 邏輯運算
score = 85
if score >= 80 and score <= 100:
    print("成績優秀")
if score > 90 or score == 85:
    print("通過")

"""
todo: 
1. 邏輯運算符: not -> 確認與寫範例
2. 把範例看完, 可稍微變更值做嘗試
"""


# # ========================================
# # 進階範例 1: 使用者登入驗證系統
# # ========================================
# print("\n--- 登入驗證系統 ---")
# username = "john_doe"
# password = "pass123"
# login_attempts = 2

# if username == "" or password == "":
#     print("錯誤: 用戶名和密碼不能為空")
# elif len(password) < 6:
#     print("錯誤: 密碼必須至少6個字符")
# elif login_attempts > 3:
#     print("錯誤: 登入嘗試次數過多，帳戶已鎖定")
# elif username == "john_doe" and password == "pass123":
#     print("✓ 登入成功")
# else:
#     print("✗ 用戶名或密碼錯誤")

# # ========================================
# # 進階範例 2: 計算BMI指數和健康建議
# # ========================================
# print("\n--- BMI 計算器 ---")
# height = 1.75  # 公尺
# weight = 70    # 公斤
# bmi = weight / (height ** 2)

# print(f"身高: {height}m, 體重: {weight}kg")
# print(f"BMI: {bmi:.1f}")

# if bmi < 18.5:
#     print("狀況: 過輕")
#     advice = "建議增加營養和運動"
# elif bmi < 24.9:
#     print("狀況: 正常")
#     advice = "保持目前的生活習慣"
# elif bmi < 29.9:
#     print("狀況: 過重")
#     advice = "建議控制飲食和增加運動"
# else:
#     print("狀況: 肥胖")
#     advice = "建議諮詢醫生和營養師"

# print(f"建議: {advice}")

# # ========================================
# # 進階範例 3: 簡單的遊戲 - 猜數字
# # ========================================
# print("\n--- 猜數字遊戲 ---")
# secret_number = 42
# guess = 35

# if guess == secret_number:
#     print("🎉 恭喜！你猜對了!")
# elif guess < secret_number:
#     print("提示: 太小了，試試更大的數字")
#     if secret_number - guess > 10:
#         print("差距很大喔")
# else:  # guess > secret_number
#     print("提示: 太大了，試試更小的數字")
#     if guess - secret_number > 10:
#         print("差距很大喔")

# # ========================================
# # 進階範例 4: 考試成績評級系統
# # ========================================
# print("\n--- 成績評級系統 ---")
# exam_score = 88
# attendance = 95  # 出席率
# participation = True  # 是否參與課堂

# # 複雜的條件判斷
# if exam_score >= 90:
#     base_grade = "A"
# elif exam_score >= 80:
#     base_grade = "B"
# elif exam_score >= 70:
#     base_grade = "C"
# elif exam_score >= 60:
#     base_grade = "D"
# else:
#     base_grade = "F"

# # 根據出席率和參與度調整成績
# if base_grade != "F":
#     if attendance < 80:
#         base_grade += "-"  # 降級
#     elif participation and attendance >= 95:
#         base_grade += "+"  # 升級

# print(f"考試成績: {exam_score}/100")
# print(f"出席率: {attendance}%")
# print(f"課堂參與: {'是' if participation else '否'}")
# print(f"最終評級: {base_grade}")

# # ========================================
# # 進階範例 5: 購物折扣系統
# # ========================================
# print("\n--- 購物折扣計算 ---")
# purchase_amount = 2500
# is_member = True
# is_holiday = False

# # 計算折扣
# if not is_member and purchase_amount < 1000:
#     discount = 0
# elif is_member and purchase_amount < 1000:
#     discount = 0.05  # 5% 折扣
# elif not is_member and purchase_amount >= 1000 and purchase_amount < 2000:
#     discount = 0.10  # 10% 折扣
# elif is_member and purchase_amount >= 1000 and purchase_amount < 2000:
#     discount = 0.15  # 15% 折扣
# elif purchase_amount >= 2000:
#     discount = 0.20 if not is_member else 0.25  # 20% 或 25%
# else:
#     discount = 0

# # 假日額外折扣
# if is_holiday and discount > 0:
#     discount += 0.05  # 額外5%

# final_price = purchase_amount * (1 - discount)
# savings = purchase_amount * discount

# print(f"原價: ${purchase_amount}")
# print(f"會員: {'是' if is_member else '否'}")
# print(f"假日: {'是' if is_holiday else '否'}")
# print(f"折扣率: {discount * 100:.0f}%")
# print(f"節省: ${savings:.2f}")
# print(f"最終價格: ${final_price:.2f}")

# # ========================================
# # 進階範例 6: 飲食推薦系統
# # ========================================
print("\n--- 飲食推薦系統 ---")
time_of_day = 14  # 24小時制
is_hungry = True
has_diet_restriction = False
restriction_type = "素食"

if not is_hungry:
    recommendation = "暫時不需要進食"
elif time_of_day >= 6 and time_of_day < 11:
    recommendation = "早餐時間: 推薦吃麥片、雞蛋或麵包"
elif time_of_day >= 11 and time_of_day < 14:
    recommendation = "午餐時間: 推薦吃米飯、麵條或漢堡"
elif time_of_day >= 14 and time_of_day < 17:
    recommendation = "下午茶時間: 推薦吃水果、餅乾或飲料"
elif time_of_day >= 17 and time_of_day < 21:
    recommendation = "晚餐時間: 推薦吃蔬菜、蛋白質或湯"
else:
    recommendation = "宵夜時間: 推薦吃清淡食物"

# 根據飲食限制調整推薦
if has_diet_restriction:
    if restriction_type == "素食":
        recommendation += " (避免肉類)"
    elif restriction_type == "無麩質":
        recommendation += " (避免麵粉製品)"
    elif restriction_type == "海鮮過敏":
        recommendation += " (避免海鮮)"

print(f"時間: {time_of_day}:00")
print(f"是否飢餓: {'是' if is_hungry else '否'}")
print(f"推薦: {recommendation}")

# not a == b 
# (not a) == b 
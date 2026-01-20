# todo: BMI運算並將結果存成list和dict 各一個程式
bmi_list = ["ryan", 1.75, 70, round(70 / (1.75 ** 2), 2)]
bmi_dict = {
    "name": "ryan",
    "height_m": 1.75,
    "weight_kg": 70,
    "bmi": round(70 / (1.75 ** 2), 2)
}
print()

# # 我需要一個使用者輸入的介面，有互動回饋的輸入框
# name = input("請輸入您的名字: ")
# height_cm = float(input("請輸入您的身高(公分): "))
# height = height_cm / 100  # 轉換成公尺
# weight = float(input("請輸入您的體重(公斤): "))

# # 驗證輸入值
# if height <= 0 or weight <= 0:
#     print("錯誤：身高和體重必須是正數！")
# else:
#     bmi = round(weight / (height ** 2), 2)
#     print(f"{name}，您的BMI是 {bmi}")


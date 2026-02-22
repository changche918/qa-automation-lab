# todo: BMI運算並將結果存成list和dict 各一個程式
# bmi_list = ["ryan", 1.75, 70, round(70 / (1.75 ** 2), 2)]
# bmi_dict = {
#     "name": "ryan",
#     "height_m": 1.75,
#     "weight_kg": 70,
#     "bmi": round(70 / (1.75 ** 2), 2)
# }
# print()

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


#
# ryan_bmi = 19
# amy_bmi = 20
# leo_bmi = 21
# bmi_list = [ryan_bmi, amy_bmi, leo_bmi]
# print(bmi_list)

ryan_high = 175
ryan_weight = 70
amy_high = 160
amy_weight = 50
leo_high = 190
leo_weight = 80
ryan_bmi = ryan_weight / (round((ryan_high / 100) ** 2),2)
amy_bmi = amy_weight / (round((amy_high / 100) ** 2),2)
leo_bmi = leo_weight / (round((leo_high / 100) ** 2),2)
# print([ryan_bmi, amy_bmi, leo_bmi])
person_bmi1 = [ryan_bmi,amy_bmi,leo_bmi]
print(person_bmi1)
person_bmi2 = {
  "ryan": ryan_bmi,
  "amy": amy_bmi,
  "leo": leo_bmi}
print(person_bmi2)

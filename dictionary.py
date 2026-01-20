# ========================================
# 3. DICTIONARIES - 字典（鍵值對）
# ========================================
# 基本用法: dict() 或 {key1: value1, key2: value2, ...}
# - 字典是無序的、可修改的、有鍵值對
# - 鍵必須是不可變類型 (字符串、數字、元組)
# - 值可以是任何類型
# - 鍵是唯一的，重複鍵會覆蓋
# - 常用方法: keys(), values(), items(), get(), pop(), update()

from webbrowser import get


print("3. DICTIONARIES 字典")
student = {
    "name": "John",
    "age": 20,
    "major": "Computer Science"
}

print(student)
print(student["name"])           # 訪問值
print(student.get("age"))        # 安全訪問

# 此三個常搭配for loop使用
print(student.keys())            # 所有鍵
print(student.values())          # 所有值
print(student.items())           # 鍵值對

student["age"] = 21              # 修改值
# print(student)
student["gpa"] = 3.8             # *** 新增 ***
# print(student)
student.pop("major")             # 刪除
# print(student)
"""
todo:
- 1.get() 使用方式 預設值範例
my = {"name": "ryan", "age": "20"}
print(my.get("name")) # 正確示範
- 2.簡單應用 keys(), values(), items()
person = {"name": "Ryan", "age": 35}
# keys
for k in person.keys():
    print(k)
# values
for v in person.values():
    print(v)
# items
for k, v in person.items():
    print(f"{k} -> {v}")
- 3.update() 嘗試用法
"""
person = {"name": "Ryan", "age": 35}
for k, v in person.items():
    print(f"{k} -> {v}")

person = {"name": "Ryan", "age": 35}

# 更新 age，新 key salary 加入
person.update({"age": 36, "salary": 40000})
print(person)

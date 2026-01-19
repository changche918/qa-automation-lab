# ========================================
# 2. LISTS - 列表（有序、可修改）
# ========================================
# 基本用法: list() 或 [item1, item2, ...]
# - 列表是有序的、可修改的、允許重複
# - 可以包含不同類型的元素
# - 常用方法: append(), remove(), pop(), insert(), extend(), clear()
# - 常用屬性: len(list)

print("2. LISTS 列表")
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

print(fruits)
print(fruits[0])        # 索引訪問
print(fruits[-1])       # 反向索引 (最後一個)
print(fruits[0:2])      # 切片

# fruits.get(0)          # 錯誤示範，列表無get方法, 只有字典(dict)有
# print(fruits['apple'])  # 錯誤示範，列表索引必須是整數

fruits.append("orange") # 新增元素
# print(fruits)
fruits.remove("banana") # 刪除元素
# print(fruits)
fruits.pop()            # 刪除最後一個
# print(fruits)
fruits.insert(1, "kiwi")# 在指定位置插入
print(fruits)

# 非常重要: len() 函數獲取列表長度 & 使用 in 判斷元素是否存在
print(f"列表長度: {len(fruits)}")
print(f"apple在列表中: {'apple' in fruits}")
print(f"Apple在列表中: {'Apple' in fruits}")


"""
TODO:
- 查extend(), clear() 用法並補充範例
- 陣列使用 [-?:-?] 進行切片範例
- string [x:x] 嘗試使用
- list() 查看使用方式
"""


# ========================================
# 3. DICTIONARIES - 字典（鍵值對）
# ========================================
# 基本用法: dict() 或 {key1: value1, key2: value2, ...}
# - 字典是無序的、可修改的、有鍵值對
# - 鍵必須是不可變類型 (字符串、數字、元組)
# - 值可以是任何類型
# - 鍵是唯一的，重複鍵會覆蓋
# - 常用方法: keys(), values(), items(), get(), pop(), update()

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
student.pop("major1")             # 刪除
# print(student)
"""
TODO:
- get() 使用方式 預設值範例
- 簡單應用 keys(), values(), items()
- update() 嘗試用法
"""
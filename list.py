# ========================================
# 2. LISTS - 列表（有序、可修改）
# ========================================
# 基本用法: list() 或 [item1, item2, ...]
# - 列表是有序的、可修改的、允許重複
# - 可以包含不同類型的元素
# - 常用方法: append(), remove(), pop(), insert(), extend(), clear()
# - 常用屬性: len(list)

# print("2. LISTS 列表")
# fruits = ["apple", "banana", "cherry"]
# numbers = [1, 2, 3, 4, 5]
# mixed = [1, "hello", 3.14, True]

# print(fruits)
# print(fruits[0])        # 索引訪問
# print(fruits[-1])       # 反向索引 (最後一個)
# print(fruits[0:2])      # 切片

# # fruits.get(0)          # 錯誤示範，列表無get方法, 只有字典(dict)有
# # print(fruits['apple'])  # 錯誤示範，列表索引必須是整數

# fruits.append("orange") # 新增元素
# # print(fruits)
# fruits.remove("banana") # 刪除元素
# # print(fruits)
# fruits.pop()            # 刪除最後一個
# # print(fruits)
# fruits.insert(1, "kiwi")# 在指定位置插入
# print(fruits)

# # 非常重要: len() 函數獲取列表長度 & 使用 in 判斷元素是否存在
# print(f"列表長度: {len(fruits)}")
# print(f"apple在列表中: {'apple' in fruits}")
# print(f"Apple在列表中: {'Apple' in fruits}")


"""
todo:
- 1.查extend(), clear() 用法並補充範例
extend()  > 純粹加元素
a = [1, 2, 3]
b = [4, 5]

a.extend(b)
print(a)

---

clear() > 清空 list，所以會變成空 list
nums = [10, 20, 30]
nums.clear()

print(nums)

- 2.陣列使用 [-?:-?] 進行切片範例
name = ['ryan' ,'lisa']
print(name[-1:-1]) 

- 3.string [x:x] 嘗試使用
name = "ryan"
print(name[1:4])
- 4.list() 查看使用方式
a = []
b = list(a)
"""
print('範例看這')
a = ['ryan', 'lisa', 'mike']
b = list(a)
print(b)
list('123')
print(list('123')) 
print(list((1,2,3)))
print(list([[1,2,3]]))
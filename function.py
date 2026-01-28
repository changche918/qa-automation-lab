# ========================================
# 6. FUNCTIONS - 函數
# ========================================
# 基本用法: def function_name(parameters): ...
# - 參數: positional arguments (位置參數), keyword arguments (關鍵字參數)
# - 預設參數: def func(a, b=default)
# - *args: 接收任意數量的位置參數 (作為元組)
# - **kwargs: 接收任意數量的關鍵字參數 (作為字典)
# - return: 返回值 (可以返回多個值)
# - lambda: 匿名函數，用於簡單的函數表達式

print("6. FUNCTIONS 函數")

# 基本函數
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))

# 多個參數
def add(a, b):
    return a + b

print(f"5 + 3 = {add(5, 3)}")

# 預設參數
def power(base, exp=2, mode=None):
    if mode == 'api':
        print("API 模式啟用")
        return {"result": base*2 ** exp}
    return base ** exp
    
print(f"程式使用新功能 = {power(3, 2, 'api')}")
print(f"2 的 3 次方 = {power(2, 3)}") #apply to app
print(f"5 的平方 = {power(5)}")

# 嘗試搞懂這兩個用法 *args 和 **kwargs
def sum_all(*numbers):
    return sum(numbers)

print(f"Sum: {sum_all(1, 2, 3, 4, 5)}")

def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="John", age=25, city="Taipei")


# 匿名函數 (lambda)
square = lambda x: x ** 2
print(f"3 的平方 = {square(3)}")

# map, filter 
"""可請AI幫忙解釋, 寫成def對照"""
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Double: {doubled}")

even = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even}")

# ========================================
# 稍微進階
# ========================================
print("\n--- 稍微進階 ---")

# 1. 函數返回另一個函數
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

times_3 = make_multiplier(3)
print(f"5 × 3 = {times_3(5)}")

# 2. 使用 reduce 計算累積值
from functools import reduce
nums = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, nums)
print(f"1+2+3+4+5 = {total}")

# ========================================
# 一點點進階
# ========================================
print("\n--- 一點點進階 ---")

# 1. 傳遞函數作為參數
def apply_func(func, a, b):
    return func(a, b)

def add_two(x, y):
    return x + y

print(f"apply_func(add_two, 10, 5) = {apply_func(add_two, 10, 5)}")

# 2. 簡單的裝飾器
"""問AI"""
def my_print(func):
    def wrapper():
        print("--- 開始 ---")
        func()
        print("--- 結束 ---")
    return wrapper

@my_print
def say_hi():
    print("Hello!")

say_hi()
# TODO: 嘗試搞懂這兩個用法 *args 和 **kwargs & 變形 (a, b, **info) 
# TODO: 嘗試 map, filter, L54~L61
# TODO: 嘗試lambda複雜一點的內容
# TODO: 範例區塊要實作與常識, L63~L110
# TODO: Preview classes (AI)

""" ========= 將功課與筆記紀錄在下方 ========= """
# todo 1 args kwargs
def name(*args):
    print(args)
name('ryan', 'jason')

def qa(**kwargs):
    print(kwargs)
qa(name="Ryan", age=35, job="QA")

# todo 2 map, filter 
print("map, filter")
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(f"Double: {doubled}")

even = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Even numbers: {even}")

nums = [1, 2, 3, 4]
result = []

for n in nums:
    result.append(n * n)

print(result)

# todo 3 lambda
num1  = lambda x,y : x + y
print(num1(5, 10))

num2 = lambda x: x if x > 0 else 0
print(num2(-5))
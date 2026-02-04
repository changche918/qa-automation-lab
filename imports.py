# ========================================
# 8. IMPORTS - 匯入模組
# ========================================
# 基本用法:
#   import module_name: 匯入整個模組
#   from module import name: 匯入模組中的特定項目
#   import module as alias: 使用別名
#   from module import *: 匯入所有項目 (不推薦)
# - 常用內建模組: math, datetime, random, json, os, sys, collections
# - 模組搜尋路徑: sys.path
# - __name__ == '__main__': 檢查是否直接運行

print("8. IMPORTS 匯入模組")

import math
print(f"π = {math.pi}")
print(f"sqrt(16) = {math.sqrt(16)}")

from datetime import datetime
now = datetime.now()
print(f"Current time: {now}")

import random
print(f"Random number: {random.randint(1, 100)}")

# 別名匯入
import json as json_module
data = json_module.dumps({"name": "John", "age": 30})
print(f"JSON: {data}")



# 创建一个自定义模块结构
# 假设目录结构:
# my_project/
#   ├── main.py
#   └── utilities/
#       ├── __init__.py
#       ├── math_helper.py
#       └── string_helper.py

# 在 utilities/math_helper.py 中:
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class Calculator:
    def __init__(self, name):
        self.name = name
    
    def calculate(self, x, y, operation):
        if operation == 'add':
            return add(x, y)
        elif operation == 'multiply':
            return multiply(x, y)

# 在 main.py 中使用:
# from utilities.math_helper import add, multiply, Calculator

# 使用导入的函数
print(add(5, 3))  # 输出: 8

# 使用导入的类
calc = Calculator("My Calculator")
result = calc.calculate(4, 6, 'multiply')
print(result)  # 输出: 24



"""
TODO: 
1. class繼承跨檔案使用
2. import結合..往前兩層資料夾 (自己寫範例)
3. 嘗試理解與寫範例: 
    - sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
    - sys.path.append('.')
4. selenium環境安裝

extra(想讀再讀)
1. if __name__ == '__main__': 走的原理
2. 可嘗試 from utilities.math_helper.Calculator import calculate 
"""

if __name__ == '__main__':
    print("This script is being run directly.")

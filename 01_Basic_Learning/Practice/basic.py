# # # 上升部分
# # for i in range(5):
# #     star = '*' * (2 * i + 1)
# #     print(star.center(9))

# # 下降部分
# for i in range(4, 0, -1):
#     star = '*' * (2 * i - 1)
#     print(star.center(9))

# def make_multiplier(n):
#     def multiply(x):
#         return x * n
#     return multiply
# times3 = make_multiplier(3)
# print(times3(5))  # 输出 15

# def make_multiplier(x ,n):
#     return x * n
# times3 = make_multiplier(3 ,5)
# print(times3)


# class Cat:
#     def sound(self):
#         return "meow"
# Cat.sound(self="test")
# print(Cat.sound(self="test"))

# class Rectangle:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height

#     def area(self):
#         return self.width * self.height

# class Square(Rectangle):
#     def __init__(self, side_length):
#         super().__init__(side_length, side_length)

# # square = Square(4)
# b = Rectangle(4 ,5)
# print(b.area())
# print(f"Square area: {square.area()}")

# class CustomError(Exception):
#     pass

# try:
#     # raise CustomError("這是自訂錯誤")
#     # raise 只能丟「例外物件」，raise 後面只能是：Exception 類別或是 Exception 的實例
#     raise print('test') # 會發生什麼 + 找到為什麼
# except CustomError as e:
#     print(f"捕捉異常: {e}")

# try:
#     x = int("abc")
# except ValueError:
#     print("轉換失敗")
#     raise


class MyError(Exception):
    pass

def demo(x):
    if x == 0:
        raise MyError("x 不能是 0")
    return 10 / x

try:
    print("A")
    print(demo(0))
    print("B")
except MyError:
    print("C")

finally:
    print("D")

print(__file__)

###

# n = float(input("請輸入一個數字: "))
# if n > 0:
#     print("positive")
# elif n < 0:
#     print("negative")
# else:
#     print("zero")

# score = float(input("請輸入分數: "))
# if score >= 90:
#     print("A")
# elif score >= 80:
#     print("B")
# elif score >= 70:
#     print("C")
# else:
#     print("F")

number = float(input("請輸入一個數字: "))
if number % 2 == 0 and number > 10:
    print("Even and > 10")
elif number % 2 == 0:
    print("Even")
else:
    print("Odd")
# ========================================
# 7. CLASSES - 類別（物件導向）
# ========================================
# 基本用法: class ClassName: ...
# - __init__(self, ...): 構造函數，初始化對象
# - self: 代表對象本身
# - __str__(): 返回對象的用戶友好字符串表示（給人看的）。
#   當使用 `print(obj)` 或 `str(obj)` 時會呼叫，應該易讀且簡潔。
# - __repr__(): 返回對象的開發者友好表示（給程式員看的）。
#   用於除錯與互動式環境（如 REPL），應包含足夠資訊以辨識物件，
#   在可能情況下應回傳能用來重建該物件的有效 Python 表達式。
# - 繼承: class Child(Parent): ...
# - super(): 訪問父類方法
# - TODO: 先查查看: 類別變數 vs 實例變數

print("7. CLASSES 類別")


class Person:
    # 類別變數
    species = "Homo sapiens"
    
    # 初始化方法
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 方法
    def introduce(self):
        return f"My name is {self.name}, I am {self.age} years old"

    # 特殊方法 #TODO: 1/31說
    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

# 建立物件
person_john = Person("John", 30)
print(person_john.introduce())
print(person_john)
print(f"Species: {person_john.species}") #TODO: 1/31說

# TODO: 與AI確認錯誤原因 print(Person.introduce("tets", "John", 30)) 

# TODO: 繼承
# 說明 super():
# - super() 用於在子類別中呼叫父類別的方法或建構子。
# - 常見用途是子類別在初始化時呼叫父類別的 __init__ 來設定父類別屬性。
# - 也可用來呼叫被覆寫（override）的父類別方法，例如 super().introduce()
# 範例: 下面的 Student 類別使用 super() 來初始化父類並延伸 introduce()
class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def introduce(self):
        return super().introduce() + f", Student ID: {self.student_id}"

student = Student("Alice", 20, "S12345")
print(student.introduce())

# 其他非常簡單的範例（給初學者）
# 範例 1: Car 類別（簡單方法）
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def drive(self):
        return f"{self.make} {self.model} is driving."

car = Car("Toyota", "Corolla")
print(car.drive())

# 範例 2: Rectangle 與 Square（示範繼承與 super()）
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side_length):
        super().__init__(side_length, side_length)

square = Square(4)
print(f"Square area: {square.area()}")
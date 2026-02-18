import os
from datetime import datetime

# class LogHandle:
#     def __init__(self, filename, data, content):
#         self.filename = filename
#         self.data = data
#         self.content = content
#     # def elem_dict(self, data):

#     def read(self):
#         with open(self.filename, "r", encoding="utf-8") as file:
#             self.content = file.read()
#     def save(self, data, filename):
#         # with open(filename, "w", encoding="utf-8") as file:
#         #     json.dump(data, file, indent = 4, ensure_ascii=False)
#         #     print(f"{filename} 儲存完成")
#         with open(filename, "w", encoding="utf-8") as file: # 如果 log 存在，且標題不一樣，就寫入
#             now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # AI 提供
#             file.write(f"[{now_time}] {data}\n") #　AI 提供

### 修改後 ###
class LogHandle:
    def __init__(self, filename, data=None, content=None):
        self.filename = filename
        self.data = data
        self.content = content

    def read(self):
        # 檢查檔案是否存在，避免程式崩潰
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                self.content = file.read()
                return self.content
        else:
            print(f"警告：找不到檔案 {self.filename}")
            return None

    def save(self, data):
        # 直接使用初始化時的 self.filename，或是從外面傳入
        with open(self.filename, "w", encoding="utf-8") as file:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{now_time}] {data}\n")
            print(f"資料已成功寫入 {self.filename}")
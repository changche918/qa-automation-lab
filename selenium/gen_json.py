import json

class DataSaver:
    def __init__(self, title):
        self.title = title
    # def json_dict(self, data):
    #     self.data = data
    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self, file, indent=2, ensure_ascii=False)
            print(f"{filename} 儲存完成")
    def load(self, filename):
        pass
    def update(self, filename):
        pass
    def delete(self, filename):
        pass
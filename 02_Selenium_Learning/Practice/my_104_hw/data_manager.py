import json

class DataManager:
    def __init__(self, title):
        self.title = title

    # 20260222 筆記 : 以下 elem_dict 這個沒有存在必要
    # def elem_dict(self, data):
    #     self.data = data
    ###
    # # 只有在這種邏輯下才需要 elem_dict (或 set_data)
    # mgr = DataManager("MyData")
    # mgr.set_data(my_list)  # 先存進去
    # mgr.clean_data()       # 內部處理，不需要傳入 data
    # mgr.save("out.json")   # 內部存檔，不需要傳入 data


    def save(self, data, filename):
        # with open(filename, "w", encoding="utf-8") as file:
        #     json.dump(data, file, indent = 4, ensure_ascii=False)
        #     print(f"{filename} 儲存完成")
        try:
        # 嘗試使用 JSON 格式儲存
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                print(f"成功以 JSON 格式儲存至 {filename}")

        except (TypeError, ValueError):
        # 如果 data 無法被 JSON 化（例如自定義的類別物件），則改存純文字
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(data))
                print(f"資料無法轉為 JSON，已改以純文字儲存至 {filename}")
                
    def load(self, filename):
        pass
    def update(self, filename):
        pass
    def delete(self, filename):
        pass
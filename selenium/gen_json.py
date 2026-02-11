import json

class DataSaver:

    def __init__(self, title="適合你的好工作"):
        self.title = title

    def save(self, elements, filename):
        data = {
            self.title: {
                el.text: el.get_attribute("href")
                for el in elements
            }
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        print(f"{filename} 儲存完成")


# 這一行會讓 json 再包一層
# data = {"適合你的好工作": {job_list.text: job_list.get_attribute("href")for job_list in tabs}}
# with open("selenium\data_1.json", "w", encoding="utf-8") as file:
#     json.dump(data, file, indent=2, ensure_ascii=False)
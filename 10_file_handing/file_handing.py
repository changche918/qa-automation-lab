# ========================================
# 10. FILE HANDLING - 檔案處理
# ========================================
# 基本用法:
#   open(filename, mode, encoding="utf-8"): 打開文件
#   - 重要：讀寫中文檔案時，請務必加上 encoding="utf-8", TODO: 想玩的話可以試試看中文沒有utf-8或問問AI給錯誤情境
#   with open(...) as file: ... (推薦，自動關閉檔案)
# - 模式: 'r' (讀), 'w' (寫，覆蓋), 'a' (追加), 'b' (二進制) TODO: 全試試看一次
# - 常用方法: read(), readline(), readlines(), write(), writelines() TODO: 全試試看一次
# - 重要: 使用 with 語句確保文件被正確關閉
# - JSON: json.dump(), json.load(), json.dumps(), json.loads()
#TODO: 整理github folder(規劃)
print("10. FILE HANDLING 檔案處理")

# 寫入檔案
with open("example.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("This is a test file.\n")

# 讀取檔案
with open("example.txt", "r") as file:
    content = file.read()
    print(f"File content:\n{content}")

# 逐行讀取
with open("example.txt", "r") as file:
    for line in file:
        print(f"Line: {line.strip()}")

# 追加內容
with open("example.txt", "a") as file:
    file.write("Appended line.\n")

# 讀取所有行
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(f"Total lines: {len(lines)}")


# 1. 寫入檔案 (Overwrite)
with open("note.txt", "w", encoding="utf-8") as f:
    f.write("這是我的第一行筆記。\n")
    f.write("學習 Python 檔案處理真有趣！")

# 2. 讀取檔案
with open("note.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("--- 讀取內容如下 ---")
    print(content)


# JSON 檔案
import json
data = {"name": "John", "age": 30, "city": "Taipei"}

with open("data.json", "w") as file:
    json.dump(data, file, indent=2)

with open("data.json", "r") as file:
    loaded_data = json.load(file)
    print(f"Loaded JSON: {loaded_data}")

"""
TODO: 玩玩看兩種
json.dumps()：轉成字串
把 Python 資料變成一串「JSON 格式的文字」。

json.loads()：文字轉回資料
把一串「符合 JSON 格式的文字」轉回 Python 的字典或列表。
"""

json_text = '{"fruit": "apple", "price": 50}'
json_text = '["text1", "text2"]'
data = json.loads(json_text) 

print(data["fruit"])  # 輸出：apple
print(data)


"""
import json

# 準備要儲存的資料 (Dictionary)
student_data = {
    "name": "小明",
    "scores": [85, 92, 78],
    "is_passed": True
}

# 1. 將資料儲存為 JSON 檔案
with open("data.json", "w", encoding="utf-8") as f:
    # indent=4 可以讓存出來的檔案漂亮好讀
    json.dump(student_data, f, indent=4, ensure_ascii=False)
print("資料已成功存入 data.json")

# 2. 從 JSON 檔案讀取資料回來
with open("data.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print(f"哈囉 {loaded_data['name']}，你的平均分數是 {sum(loaded_data['scores'])/3:.1f}")
"""
# ========================================
# 9. TRY/EXCEPT - 例外處理
# ========================================
# 基本用法: try: ... except ExceptionType: ... else: ... finally: ...
# - try: 執行可能引發異常的代碼
# - except: 捕捉和處理特定異常 (可以有多個 except)
# - else: 如果沒有異常發生則執行
# - finally: 無論是否有異常都會執行 (清理資源)
# - raise: 主動引發異常
# - TODO: 常見異常: ValueError, TypeError, ZeroDivisionError, IndexError, KeyError (查清楚)

print("9. TRY/EXCEPT 例外處理")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("錯誤: 不能除以零")
except Exception as e:
    print(f"發生錯誤: {e}")

# 多個異常
try:
    number = int("abc")
except ValueError:
    print("錯誤: 無法轉換為整數")
except TypeError:
    print("錯誤: 類型錯誤")

# else 和 finally
try:
    result = 10 / 2
except ZeroDivisionError:
    print("錯誤: 不能除以零")
else:
    print(f"結果: {result}")
finally:
    print("執行完成")

# TODO: 自訂異常 (查清楚整個)
# - raise: 主動引發異常
class CustomError(Exception):
    pass

try:
    raise CustomError("這是自訂錯誤")
    # TODO: 嘗試 raise print('test') 會發生什麼 + 找到為什麼
except CustomError as e:
    print(f"捕捉異常: {e}")
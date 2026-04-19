# Created: 2026-04-19
"""LINE 通知連線測試工具。

用途：確認 .env 設定正確、token 有效、bot 能發訊息到你的手機。
跑完如果手機 LINE 有收到「LINE 通知測試成功」的訊息，代表整個鏈路都通了。

執行方式（擇一，都從專案根目錄）：
    python side_projects/test_line.py            ← 直接執行
    python -m side_projects.test_line            ← module 方式（推薦）
"""
import sys
from pathlib import Path

# 讓 import 路徑能找到 side_projects package，無論用哪種方式執行
# Path(__file__).resolve().parent.parent = 專案根目錄
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# 先載入 .env，讓 os.environ 讀得到 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_USER_ID
load_dotenv()

from side_projects.utils.line_notifier import LineNotifier


def main() -> int:
    try:
        notifier = LineNotifier()
    except RuntimeError as e:
        print(f"❌ 環境變數沒設好：{e}")
        print("請確認：")
        print("  1. .env 檔案在專案根目錄")
        print("  2. 內容有 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_USER_ID")
        print("  3. 已執行 pip install python-dotenv")
        return 1

    try:
        notifier.send_text("✅ LINE 通知測試成功！\n你的爬蟲已經能推送訊息到手機了。")
        print("✅ 訊息已送出，請看手機 LINE 是否收到")
        return 0
    except Exception as e:
        print(f"❌ 發送失敗：{e}")

        # 把 LINE 回傳的詳細錯誤印出來，才知道到底哪裡錯
        response = getattr(e, "response", None)
        if response is not None:
            print(f"\n[LINE API 詳細回應]")
            print(f"狀態碼: {response.status_code}")
            print(f"訊息內容: {response.text}")

        # 印出目前讀到的 User ID（只印前後幾位，避免完整外洩）
        uid = notifier.user_id or ""
        masked = f"{uid[:5]}...{uid[-4:]}" if len(uid) > 10 else uid
        print(f"\n[目前使用的 User ID]: {masked}  (長度: {len(uid)})")

        print("\n常見原因：")
        print("  - 401 Unauthorized → Channel access token 貼錯或過期")
        print("  - 400 Bad Request  → User ID 格式錯，或對方還沒加 bot 為好友")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

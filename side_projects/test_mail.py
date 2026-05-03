from dotenv import load_dotenv

load_dotenv()   # 啟動時自動把 .env 的內容塞進 os.environ

from pathlib import Path
import sys
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from side_projects.utils.mailer import Mailer

send_test_mail = Mailer()
send_test_mail.send("changche918@gmail.com", "測試", "Hello")

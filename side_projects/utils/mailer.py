# Created: 2026-05-03
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    """寄送郵件工具，使用 Gmail SMTP（SSL，port 465）。

    使用前需設定環境變數：
        GMAIL_USER    : 寄件人 Gmail 帳號
        GMAIL_APP_PWD : Google 應用程式密碼（16 字元，非登入密碼）
    """

    def __init__(self):
        """初始化寄件人帳密，從環境變數讀取以避免將密碼寫死於程式中。"""
        self.sender = os.environ["GMAIL_USER"]
        self.password = os.environ["GMAIL_APP_PWD"]

    def send(self, to_addr, subject, body, attach_path=None):
        """寄送一封郵件，可選擇是否附加檔案。

        Args:
            to_addr: 收件人 Email。
            subject: 郵件主旨。
            body: 郵件內文（純文字，UTF-8）。
            attach_path: 附件檔案路徑，若不需附件則傳 None。
        """
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        if attach_path:
            self._attach_file(msg, attach_path)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender, self.password)
            server.send_message(msg)

    def _attach_file(self, msg, file_path):
        """將指定檔案以附件形式加入郵件。

        Args:
            msg: 已建立的 MIMEMultipart 物件。
            file_path: 要附加的檔案路徑。
        """
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(file_path)}"',
        )
        msg.attach(part)

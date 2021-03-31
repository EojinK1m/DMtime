import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header


class EmailSender:
    def __init__(
        self,
        sender_email_address=None,
        password=None,
        smtp_server_address=None,
        port=None,
    ):
        self.sender_email_address = sender_email_address
        self.password = password
        self.smtp_server_address = smtp_server_address
        self.port = port
        self.testing = None

    def init_app(self, app):
        self.sender_email_address = app.config["EMAIL_SENDER_ADDRESS"]
        self.password = app.config["EMAIL_PASSWORD"]
        self.smtp_server_address = app.config["EMAIL_SERVER"]
        self.port = app.config.get("EMAIL_PORT", 587)
        self.testing = app.config["TESTING"]
        self.check_connection()

    def check_connection(self):
        if self.testing:
            return

        try:
            with smtplib.SMTP(self.smtp_server_address, self.port) as smtp:
                smtp.ehlo()
        except Exception as e:
            raise Exception(
                f"smtp server address : {self.smtp_server_address}, port : {self.port}"
            )

    def send_mail(self, to_email, message):
        if self.testing:
            return

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.smtp_server_address, self.port) as smtp:
                smtp.ehlo()
                smtp.starttls(context=context)
                smtp.login(self.sender_email_address, self.password)
                smtp.sendmail(self.sender_email_address, to_email, message)
        except smtplib.SMTPException as e:
            raise e

    def make_mail(self, subject, message):
        message = MIMEText(message, "plain", "utf-8")
        message["Subject"] = Header(subject, "utf-8")

        return message.as_string()

import smtplib, email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_host = "smtp.gmail.com"
smtp_port = 587

login_account = "y200090@mail.ryukoku.ac.jp"
login_password = "eldftuwdzjarzuvq"

# 件名
subject = "英単語学習アプリの初回ログイン"
# 送信元メールアドレス
from_email = "y200090@mail.ryukoku.ac.jp"
# 送信先メールアドレス
to_email = "kk112331@icloud.com"
# 本文
body_text = '''
こんにちは
さようなら
'''

message = MIMEMultipart()
message["Subject"] = subject
message["From"] = email.utils.formataddr(('PROJECT RESEARCH', from_email))
message["To"] = to_email
message.attach(MIMEText(body_text, 'plain', 'utf-8'))

server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
server.login(login_account, login_password)
server.send_message(message)
server.quit()

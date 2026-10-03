import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls() 

server.ehlo()

with open("password.txt") as f:
    password = f.read()

# print(password)

server.login("thinkdifferent782@gmail.com", password=password)

msg = MIMEMultipart()

msg['From'] = "test_1"
msg['To'] = "loyife3703@bowlfuel.com"
msg['Subject'] = 'Just random Shit'

with open("message.txt") as f:
    message = f.read()

msg.attach(MIMEText(message, "plain"))

filename = 'vllm.png'
attachment = open(filename, 'rb')

p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)

p.add_header("Content-Disposition", f'attachment; filename={filename}')
msg.attach(p)

text = msg.as_string()

server.sendmail('thinkdifferent782@gmail.com', 'loyife3703@bowlfuel.com', text)
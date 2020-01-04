#coding=utf-8

import smtplib
from email.mime.multipart import MIMEMultipart #email內容載體
from email.mime.text import MIMEText #用於製作文字內文
from email.mime.image import MIMEImage #用於圖檔
from email.mime.base import MIMEBase #用於承載附檔
from email import encoders #用於附檔編碼

#設定要使用的Gmail帳戶資訊
gmail_user = ''
gmail_password = ''

# 設定寄件資訊
from_address = gmail_user
to_address = ['']
Subject = "植物的一天"
contents = "這是今天植物土壤濕度監測跟環境溫度濕度,還有它可愛的照片(*ﾟ∀ﾟ*)"
attachments = ['soildata.png','plant.png']

#開始組合信件內容
mail = MIMEMultipart()
mail['From'] = from_address
mail['To'] =', '.join(to_address)
mail['Subject'] = Subject

#將信件內文加到email中
mail.attach(MIMEText(contents))

#將附加檔案們加到email中
for file in attachments:
    with open(file, 'rb') as fp:
        add_file = MIMEBase('application', "octect-stream")
        add_file.set_payload(fp.read())

    encoders.encode_base64(add_file)
    add_file.add_header('Content-Disposition','attachment', filename=file)
    mail.attach(add_file)

#設定smtp伺服器並寄發信件
smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465)
smtpserver.ehlo()
smtpserver.login(gmail_user,gmail_password)
smtpserver.sendmail(from_address,to_address,mail.as_string())
smtpserver.quit()
print('郵件傳送成功')

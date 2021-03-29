from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from email.mime.application import MIMEApplication
from os.path import basename
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def kodo_mail(name, mail, kodo):
    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587

    bodys = name + "様\n認証コードを送付します。\n" + kodo + "\n登録画面に入力してください。"
    body = bodys.replace("\n", "<br>")

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "認証コード"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()

def toroku_mail(mail, name):
    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587

    bodys = name + "様\n登録完了です。"
    body = bodys.replace("\n", "<br>")

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "登録完了お知らせ"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()


def reset_mail(mail,kodo):
    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587

    bodys = "パスワードリセット用のURLを送付します。\n" + "http://127.0.0.1:5000/reset?rand=" + kodo
    body = bodys.replace("\n", "<br>")

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "パスワードリセット用URL"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()

def henkou_mail(mail):
    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587

    bodys = "パスワードを変更しました。"
    body = bodys.replace("\n", "<br>")

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "パスワードリセット"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()



def send_mail(data,price,product_list):
    result = pdf(price,product_list)

    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587
    body_text = data[1] + "様" + "\nお買い上げありがとうございます。" + "\n請求書を送付いたします"
    body = body_text.replace("\n", "<br>")
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "お買い上げ完了のお知らせ"
    msg["From"] = ID
    msg["To"] = data[2]

    name = basename(result)
    with open(result, "rb") as f:
        attachment = MIMEApplication(f.read(), Name = name)
    attachment.add_header("Content-Disposition", "attachment", filename = name)

    msg.attach(attachment)

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()

def pdf(price,product_list):
    file = "請求書.pdf"
    file_path = os.path.expanduser("~") + "/Desktop/" + file
    page = canvas.Canvas(file_path, pagesize = portrait(A4))

    pdfmetrics.registerFont(TTFont("HGRGE", "C:/Windows/Fonts/HGRGE.TTC"))

    width,height = A4
    page.setFont("HGRGE", 60)
    page.drawCentredString(width / 2, 750, "請求書")
    page.setLineWidth(3)
    page.rect(20, 120, 550, 600)
    page.setFont("HGRGE", 20)
    h = 680
    for i in product_list:
        page.drawString(30,h,"・" + i[1] + "  ￥" + str(i[3]*i[4]) + "  " + str(i[4]) + "個")
        h -= 30

    page.setFont("HGRGE", 30)
    page.drawRightString(550, 30, "請求金額" + str(price) + "円")

    page.save()
    return file_path

def account_mail(mail, name):
    ID = "*****"
    PASS = "*****"
    HOST = "smtp.gmail.com"
    PORT = 587

    bodys = name + "様\nユーザー情報を変更しました。"
    body = bodys.replace("\n", "<br>")

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))

    msg["Subject"] = "変更のお知らせ"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()
    server.login(ID, PASS) 
    server.send_message(msg)

    server.quit()


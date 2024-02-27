import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(sender,receiver,subject,send_msg,smtpserver='smtp.qq.com',password="hdwbuuixiuzzdifh"):
    # sender = '2240551797@qq.com'
    # receiver = '1729362897@qq.com'
    # smtpserver = 'smtp.qq.com'

    # password = 'hdwbuuixiuzzdifh'

    # subject = '验证码'
    msg = MIMEText(send_msg, 'plain', 'utf-8')

    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    # print(msg.as_string())

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

if __name__ == "__main__":
    # run()
    # run2()

    send_email
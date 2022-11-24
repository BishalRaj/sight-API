from email.message import EmailMessage
from decouple import config
import ssl
import smtplib


def sendEmail(reciever, subject, body):
    email_sender = config("sender_email")
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = reciever
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, config("sender_pwd"))
        smtp.sendmail(email_sender, reciever, em.as_string())

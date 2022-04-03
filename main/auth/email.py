from main import mail
from flask import current_app
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)




def send_email(subject, sender, bcc, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, bcc=bcc, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(reader):
    token = reader.get_reset_password_token()
    send_email('[Bookstore] Reset Your Password',
               sender= 'support.bookstore@muhammadnasr.com',
               bcc= ['bookstore@muhammadnasr.com'],
               recipients=[reader.email],
               text_body=render_template('email/reset_password.txt',
                                         reader=reader, token=token),
               html_body=render_template('email/reset_password.html',
                                         reader=reader, token=token))
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
import threading
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    print("主题：%s", app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject)
    print("sender:%s",app.config['FLASKY_MAIL_SENDER'])
    print("recivier:%s",[to])

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    print(msg)
    print(msg.body)
    print(msg.html)


    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

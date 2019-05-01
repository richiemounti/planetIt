from app.decorators import aasync
from app.extensions import mail
from flask_mail import Message


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(app, subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    send_async_email(app, msg)
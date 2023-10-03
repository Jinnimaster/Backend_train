from flask_mail import Mail, Message

mail = Mail()
def send_mail(title, body, from_p, to_p):

    msg = Message(body = body,
                  subject = title,
                  sender = from_p,
                  recipients=to_p)
    mail.send(msg)

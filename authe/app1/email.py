from django.core.mail import send_mail
from django.conf import settings


def send_mail_password(email, token):

    subject = ' Password reset'
    message = f'resert the password by clicking on the link: http://127.0.0.1:8000/resetpassword/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    send_mail(subject , message, email_from, recipient_list)
    return True

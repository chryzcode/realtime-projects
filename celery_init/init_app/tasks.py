# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def my_task(arg1, arg2):
    # Task logic here
    result = arg1 + arg2
    return result


@shared_task
def test_send_mail():
    send_mail(
        subject = "A Test",
        message = "",
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = ['test@gmail.com',],
        html_message=f"""
       <h3> Hello, </h3>
       <p>
       How you doing
        </br> See you later
        </p>
        """,
        fail_silently=False,
    )



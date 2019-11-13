from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage

@shared_task
def send_mail(subject, body, to):
    return EmailMessage(subject=subject, body=body, to=[to]).send()
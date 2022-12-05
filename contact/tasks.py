from django.core.mail import send_mail
from Films.celery import app


from .service import send
from .models import Contact



@app.task
def send_spam_mail(user_mail):
    send(user_mail)


from django.core.mail import send_mail





def send(user_email):
    send_mail(
            'You are subscribed on spam',
            'We will send you ton of spam',
            'razerresolution@gmail.com',
            [user_email],
            fail_silently=False,
            )

    

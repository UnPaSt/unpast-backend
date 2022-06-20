from django.core.mail import send_mail
from settings import settings

sender = settings.EMAIL_HOST_USER

def server_startup():
    send_mail('Encore system startup', f'The encore backend is now ready!', sender,
              ['status@andimajore.de'], fail_silently=False)


def error_notification(message):
    send_mail('Error in encore-execution', f'Message: {message}', sender,
              ['status@andimajore.de'], True)

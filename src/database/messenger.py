from django.core.mail import send_mail
from settings import settings

sender = settings.EMAIL_ADDRESS


def server_startup():
    send_mail('UnPaSt system startup', f'The UnPaSt backend is now ready!', sender,
              ['status@andimajore.de'], fail_silently=False)


def error_notification(message):
    send_mail('Error in UnPaSt execution', f'Message: {message}', sender,
              ['status@andimajore.de'], True)


def get_notification_mail(id):
    from database.models import Mail
    try:
        mails = []
        for n in Mail.objects.filter(uid=id):
            mails.append(n.mail)
        return mails
    except Exception:
        print("No mailing entries fround for ID=" + id)
        return None


def remove_notification(id):
    from database.models import Mail
    for n in Mail.objects.filter(uid=id):
        n.delete()


def send_notification(mail, error, uid=None):
    try:
        if not error:
            link = f"https://unpast.zbh.uni-hamburg.de/result/{uid}"
            send_mail('Your job has finished',
                      f'The UnPaSt bicluster computation has finished.\nCheck the results out here: {link}', sender,
                      [mail],
                      fail_silently=False)
        else:
            send_mail('Your job exited with an error',
                      f'The UnPaSt bicluster computation has terminated with an error.\n Please try again or contact the authors.',
                      sender, [mail], fail_silently=False)
    except Exception as e:
        print(f"UnPaSt mailing service encountered an issue: {e}")
        error_notification(f"UnPaSt mailing service encountered an issue: {e}")

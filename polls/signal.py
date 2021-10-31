import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip_addr = get_client_ip(request)
    logger.info(f"{user} logged in from {ip_addr}")


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    print("asdf")
    ip_addr = get_client_ip(request)  
    logger.info(f"{user} logged out from {ip_addr}")


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    print("1234")
    logger.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))
from __future__ import absolute_import, unicode_literals
import logging
import sys
sys.path.append('../')
from celery import shared_task
from conf.project_conf import EMAIL_SETTING
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework_simplejwt.authentication  import JWTAuthentication
from account.models import User

logger = logging.getLogger(__name__)

def rand_str(len=32, type=None):
    res_str = ''
    if type == 'num':
        res_str = get_random_string(length=len, allowed_chars="1234567890")
    else:
        res_str = get_random_string(length=len, allowed_chars="1234567890abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ")
    return res_str

def get_user_and_token_by_jwt_request(request):
    user, token = JWTAuthentication().authenticate(request=request)
    return user, token

@shared_task
def async_send_email(subject, message, recipient_list):
    try:
        send_mail(subject=subject, from_email=EMAIL_SETTING['EMAIL_FROM'], message=message, recipient_list=recipient_list, fail_silently=False)
    except Exception as e:
        logger.exception(e)

def get_user_by_ws(header):
    headers = {}
    for v in header:
        headers[v[0].decode('utf-8')] = v[1].decode('utf-8').encode('iso-8859-1')
    auth = JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(auth.get_raw_token(headers['authorization']))
    except Exception as e:
        raise e
    user_id = validated_token['user_id']
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        return None
    return user
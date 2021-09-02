from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests

from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse((
        'https',
        'api.vk.com',
        '/method/user.get',
        None,
        urlencode(OrderedDict(
            fields=','.join(('bdate', 'sex', 'about')),
            access_token=response['access_token'],
            v='5.131')),
        None
    ))
    response = requests.get(api_url)
    if response.status_code != 200:
        return

    user_profile_data = response.json()['response'][0]
    if user_profile_data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if user_profile_data['sex'] == 2 else ShopUserProfile.FEMALE

    if user_profile_data['about']:
        user.shopuserprofile.about_me = user_profile_data['about']

    if user_profile_data['bdate']:
        bdate = datetime.strptime(user_profile_data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()


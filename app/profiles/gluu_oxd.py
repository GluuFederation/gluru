import requests
import logging
import os
import oxdpython
import configparser
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from profiles.models import UserProfile
from django.core.cache import cache

__author__ = 'centroxy'


logger = logging.getLogger(__name__)
config_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings.OXD_CFG)

class Struct:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

class AuthBackend:

    def authenticate(self, access_token, password=False):
        oxc = oxdpython.Client(config_location)
        response = oxc.get_user_info(access_token)
        user_details = get_user_details(response)
        del oxc
        user, _ = UserProfile.objects.get_or_create(email=user_details['email'])
        user.username = user_details['username']
        user.save()
        return user

    def get_user(self, user_id):
        return UserProfile.objects.get(id=user_id)


def authorize(request):
    oxc = oxdpython.Client(config_location)
    config = configparser.ConfigParser()
    config.read(config_location)
    if cache.get(settings.OXD_CLIENT_TOKEN) is None:
        client_token = oxc.get_client_token(auto_update=False)
        cache.set(settings.OXD_CLIENT_TOKEN, client_token, timeout=settings.OXD_CLIENT_TOKEN_TIMEOUT)

    authorization_url = oxc.get_authorization_url()
    del oxc
    return redirect(authorization_url)


def callback(request):
    try:
        oxc = oxdpython.Client(config_location)
        code = request.GET.get('code')
        state = request.GET.get('state')
        tokens = oxc.get_tokens_by_code(code, state)
        del oxc
    except:
        return redirect("/")
    user = authenticate(access_token=tokens['access_token'])

    if user:
        login(request, user)
    return redirect("/")

def get_user_details(response):
    return {
        'username': response['name'][0] if 'name' in response else '',
        'email': response['email'][0] if 'email' in response else '',
        'fullname': response['name'][0] if 'name' in response else '',
        'first_name': response['given_name'][0] if 'given_name' in response else '',
        'last_name': response['family_name'][0] if 'family_name' in response else ''
    }


def get_logout(request):
    oxc = oxdpython.Client(config_location)
    if cache.get(settings.OXD_CLIENT_TOKEN) is None:
        client_token = oxc.get_client_token(auto_update=False)
        cache.set(settings.OXD_CLIENT_TOKEN, client_token, timeout=settings.OXD_CLIENT_TOKEN_TIMEOUT)
    logout_url = oxc.get_logout_uri()
    del oxc
    logout(request)

    return redirect(logout_url)


def setup_client(request, render_page=True):
    oxc = oxdpython.Client(config_location)
    response = {}
    if request.method == 'POST':
        try:
            client = oxc.setup_client()
            response = get_client(client)
        except Exception as e:
            return {"status": "ko","message": e}
        del oxc
    else:
        response = registered_client()
    return render(request, "setup.html", {'response': response}) if render_page else response

def get_client(response):
    message = "Client Setup failed."
    status = "error"
    if response['oxd_id']:
        status = "ok"
        message = "Client Setup successful!!"
    return {
        'oxd_id': response['oxd_id'],
        'setup_client_oxd_id':response['setup_client_oxd_id'],
	'client_id': response['client_id'],
        'client_secret': response['client_secret'],
        'client_secret_expires_at': response['client_secret_expires_at'],
	'status': status,
        'message': message
    }


def registered_client():
    oxc = oxdpython.Client(config_location)
    oxd_id = oxc.config.get("oxd", "id")
    client_id = oxc.config.get("client", "client_id")
    client_secret = oxc.config.get("client", "client_secret")
    client_secret_expires_at = oxc.config.get("client","client_secret_expires_at")
    del oxc
    if oxd_id and client_id and client_secret:
        return {'oxd_id': oxd_id,
                'client_id': client_id,
                'client_secret': client_secret,
		'client_secret_expires_at': client_secret_expires_at,
                'status': "exists",
                'message': "Client registered"}


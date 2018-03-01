import json
import logging
import random
import requests

from hashlib import sha1 as sha_constructor

from django.conf import settings

from connectors.idp.uma_access import obtain_authorized_rpt_token

logger = logging.getLogger('idp')

# noinspection PyInterpreter
SCIM_CREATE_USER_ENDPOINT = settings.SCIM_UPDATE_USER_CONSTANT
SCIM_UPDATE_USER_ENDPOINT = settings.SCIM_UPDATE_USER_CONSTANT


def create_user(user, password, active=False):

    headers = {'Content-Type': 'application/json'}
    params = {}

    payload = {
        'schemas': ['urn:ietf:params:scim:schemas:core:2.0:User'],
        'userName': sha_constructor(str(random.random())).hexdigest()[:12],
        'name': {'givenName': user.first_name, 'familyName': user.last_name},
        'displayName': u'{}{}'.format(user.first_name, user.last_name),
        'password': password,
        'emails': [
            {'value': user.email, 'primary': True, 'type': 'Work'}
        ],
        'phoneNumbers': [
            {'value': user.mobile_number, 'primary': True, 'type': 'Work'}
        ],
        'timezone': user.timezone,
        'title': user.job_title
    }

    if active:
        payload['active'] = True

    url = SCIM_CREATE_USER_ENDPOINT

    if settings.SCIM_TEST_MODE:
        params['access_token'] = settings.SCIM_TEST_MODE_ACCESS_TOKEN

    else:
        rpt = obtain_authorized_rpt_token(resource_uri=url)
        headers['Authorization'] = 'Bearer {}'.format(rpt)

    response = requests.post(
        url,
        data=json.dumps(payload),
        verify=settings.VERIFY_SSL,
        headers=headers,
        params=params
    )

    if response.status_code != 201:
        message = 'Error writing to idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    else:
        response = response.json()
        return response['id']


def activate_user(user):

    headers = {'Content-Type': 'application/json'}
    params = {}

    url = SCIM_UPDATE_USER_ENDPOINT.format(user.idp_uuid)

    if settings.SCIM_TEST_MODE:
        params['access_token'] = settings.SCIM_TEST_MODE_ACCESS_TOKEN

    else:
        rpt = obtain_authorized_rpt_token(resource_uri=url)
        headers['Authorization'] = 'Bearer {}'.format(rpt)

    payload = {'active': True}

    response = requests.put(
        url,
        data=json.dumps(payload),
        verify=settings.VERIFY_SSL,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        message = 'Error writing to idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)


def update_user(user):

    headers = {'Content-Type': 'application/json'}
    params = {}

    if not user.idp_uuid:
        logger.error('Error writing to idp, missing uid: {}'.format(user.email))
        return

    url = SCIM_UPDATE_USER_ENDPOINT.format(user.idp_uuid)

    if settings.SCIM_TEST_MODE:
        params['access_token'] = settings.SCIM_TEST_MODE_ACCESS_TOKEN

    else:
        rpt = obtain_authorized_rpt_token(resource_uri=url)
        headers['Authorization'] = 'Bearer {}'.format(rpt)

    payload = {
        'name': {'givenName': user.first_name, 'familyName': user.last_name},
        'displayName': u'{}{}'.format(user.first_name, user.last_name),
        'phoneNumbers': [
            {'value': user.mobile_number, 'primary': True, 'type': 'Work'}
        ],
        'timezone': user.timezone,
        'title': user.job_title
    }

    response = requests.put(
        url,
        data=json.dumps(payload),
        verify=settings.VERIFY_SSL,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        message = 'Error writing to idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    else:
        logger.info('Successfully updated {}'.format(user.email))


def get_user(user):

    if not user.idp_uuid:
        logger.error('Error writing to idp, missing uid: {}'.format(user.email))
        return

    headers = {'Content-Type': 'application/json'}
    params = {}
    url = SCIM_UPDATE_USER_ENDPOINT.format(user.idp_uuid)

    if settings.SCIM_TEST_MODE:
        params['access_token'] = settings.SCIM_TEST_MODE_ACCESS_TOKEN

    else:
        rpt = obtain_authorized_rpt_token(resource_uri=url)
        headers['Authorization'] = 'Bearer {}'.format(rpt)

    response = requests.get(url, verify=settings.VERIFY_SSL, headers=headers)

    if response.status_code != 200:
        message = 'Error retrieving idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    else:
        return response.json()


def email_exists(email):

    headers = {'Content-Type': 'application/json'}

    url = SCIM_CREATE_USER_ENDPOINT

    params = {'filter': 'emails.value eq "{}"'.format(email)}

    if settings.SCIM_TEST_MODE:
        params['access_token'] = settings.SCIM_TEST_MODE_ACCESS_TOKEN

    else:
        rpt = obtain_authorized_rpt_token(resource_uri=url)
        headers['Authorization'] = 'Bearer {}'.format(rpt)

    response = requests.get(url, verify=settings.VERIFY_SSL, headers=headers, params=params)

    if response.status_code != 200:

        message = 'Error retrieving from idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    else:

        no_records = int(response.json()['totalResults'])

        if no_records not in [0, 1]:

            message = 'Unexpected number of records found for {}'.email
            logger.error(message)
            raise Exception(message)

        return no_records == 1

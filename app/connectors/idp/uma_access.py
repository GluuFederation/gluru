import logging
import requests
from main import settings
from django.conf import settings

logger = logging.getLogger('idp')


def obtain_aat():

    # https://gluu.org/docs/api/oic-token/

    payload = {
        'client_id': settings.UMA_CLIENT_ID,
        'client_secret': settings.UMA_CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'uma_authorization'

    }

    response = requests.post(
        settings.UMA_ACCESS_TOKEN_ENDPOINT,
        data=payload,
        verify=settings.VERIFY_SSL
    )

    if response.status_code == 200 and response.json()['scope'] == 'uma_authorization':

        return response.json()['access_token']

    else:

        message = 'Error during UMA Authentication: Failed to obtain AAT: {}, ({})'.format(
            response.text, response.status_code)

        logger.error(message)

        raise Exception(message)


def obtain_rpt(access_token):

    # https://gluu.org/docs/api/uma-create-rpt/

    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post(
        settings.UMA_OBTAIN_RPT,
        data={},
        headers=headers,
        verify=settings.VERIFY_SSL
    )

    if response.status_code == 201:

        return response.json()['rpt']

    else:

        message = 'Error during UMA Authentication: Failed to obtain RPT: {}, ({})'.format(
            response.text, response.status_code)

        logger.error(message)

        raise Exception(message)


def obtain_resource_ticket(rpt, resource_uri):

    headers = {'Authorization': 'Bearer {}'.format(rpt)}

    response = requests.get(
        resource_uri,
        headers=headers,
        verify=settings.VERIFY_SSL
    )

    if response.status_code != 403:

        message = 'Error during UMA Authentication: Failed to obtain ticket: {}, ({})'.format(
            response.text, response.status_code)

        logger.error(message)

        raise Exception(message)

    else:
        return response.json()['ticket']


def authorize_rpt(access_token, rpt, ticket):

    # See https://gluu.org/docs/api/uma-authorization-endpoint/

    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    payload = {'ticket': ticket, 'rpt': rpt}

    response = requests.post(
        settings.UMA_AUTHORIZE_RPT,
        json=payload,
        headers=headers,
        verify=settings.VERIFY_SSL
    )

    if response.status_code != 200 or response.json()['rpt'] != rpt:

        message = 'Error during UMA Authentication: Failed to authorize rpt : {}, ({})'.format(
            response.text, response.status_code)

        logger.error(message)

        raise Exception(message)

    return rpt


def obtain_authorized_rpt_token(resource_uri=None, ticket=None):

    access_token = obtain_aat()

    rpt = obtain_rpt(access_token)

    if not ticket:
        ticket = obtain_resource_ticket(rpt, resource_uri)

    return authorize_rpt(access_token, rpt, ticket)

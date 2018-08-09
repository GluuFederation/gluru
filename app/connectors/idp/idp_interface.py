# ---------- User Registration with Gluu IDP -----------  

   # You need to build jar file for user registration
   # See the java_sample_code.java file
   # Add RPT client Id
   # Add RPT client secret
   # Add Files path in idp interface file and java_sample_code.java file
   # Add jar file path and give arrgument in idp interface file.



import json
import logging
import random
import requests
import subprocess
import json
from hashlib import sha1 as sha_constructor

from django.conf import settings

from connectors.idp.uma_access import obtain_authorized_rpt_token

logger = logging.getLogger('idp')

# noinspection PyInterpreter
SCIM_CREATE_USER_ENDPOINT = settings.SCIM_UPDATE_USER_CONSTANT
SCIM_UPDATE_USER_ENDPOINT = settings.SCIM_UPDATE_USER_CONSTANT


def create_user(user):

    headers = {'Content-Type': 'application/json'}
    params = {}

    payload = {
            'schemas': ['urn:ietf:params:scim:schemas:core:2.0:User'],
            'userName': sha_constructor(str(random.random())).hexdigest()[:12],
            'name': {'givenName': user.first_name, 'familyName': user.last_name},
            'displayName': u'{}{}'.format(user.first_name, user.last_name),
            'emails': [
                {'value': user.email, 'primary': True, 'type': 'Work'}
            ]
    }
    file = 'Path to your file'
    with open(file, 'w') as outfile:
        json.dump(payload, outfile)
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("json_string ="+ content)

    process = ['java', '-jar','Path to your jar file', 'create', '{0}'.format(user.email), '{0}'.format(user.id)]
    process = subprocess.Popen(process, stdout=subprocess.PIPE)
    response = process.communicate()[0]
    response = json.loads(response)
    if response.get('totalResults') >= 1:
        resource = response.get('Resources')[0]
        return {"user_exist": True, "uuid": resource.get('id')}
    else:
        return response.get('id')


def activate_user(user):

    payload = {
        'active': True,
        'id': user.idp_uuid
        }

    file = 'Path to your file'
    with open(file, 'w') as outfile:
        json.dump(payload, outfile)
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("json_string ="+ content)

    process = ['java', '-jar', 'Path to your jar file', 'activate_user', '{0}'.format(user.id),
               '{0}'.format(user.idp_uuid)]
    process = subprocess.Popen(process, stdout=subprocess.PIPE)
    response = process.communicate()[0]
    response = json.loads(response)
    print response
    if 'status_code' in response:
        message = 'Error writing to idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)


def update_user(user, password):

    headers = {'Content-Type': 'application/json'}
    params = {}

    if not user.idp_uuid:
        logger.error('Error writing to idp, missing uid: {}'.format(user.email))
        return
    if not password:
        payload = {
        'schemas': ['urn:ietf:params:scim:schemas:core:2.0:User'],
        'id': user.idp_uuid,
	    'active':True,
        'name': {'givenName': user.first_name, 'familyName': user.last_name},
        'phoneNumbers': [
            {'value': user.mobile_number, 'primary': True, 'type': 'Work'}
        ],
        'timezone': user.timezone,
        'title': user.job_title
    	}
    else:
       payload = {
        'schemas': ['urn:ietf:params:scim:schemas:core:2.0:User'],
        'id': user.idp_uuid,
        'active': True,
        'password': password,
        'phoneNumbers': [
            {'value': user.mobile_number, 'primary': True, 'type': 'Work'}
        ],
        'timezone': user.timezone,
        'title': user.job_title
        }
    file = 'Path to your file'
    with open(file, 'w') as outfile:
        json.dump(payload, outfile)
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("json_string =" + content)


    process = ['java', '-jar', 'Path to your jar file', 'activate_user', '{0}'.format(user.id),
               '{0}'.format(user.idp_uuid)]
    process = subprocess.Popen(process, stdout=subprocess.PIPE)
    response = process.communicate()[0]

    response = json.loads(response)
    if 'status_code' in response:
        message = 'Error writing to idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    return response



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

    process = ['java', '-jar', 'Path to your jar file', 'activate_user', '{0}'.format(email)]
    process = subprocess.Popen(process, stdout=subprocess.PIPE)
    response = process.communicate()[0]
    print response
    response = json.loads(response)
    if 'status_code' in response:
        message = 'Error retrieving from idp: {} {}'.format(response.status_code, response.text)
        logger.error(message)
        raise Exception(message)

    else:
        no_records = int(response.get('totalResults'))
        if no_records not in [0, 1]:

            message = 'Unexpected number of records found for {}'.email
            logger.error(message)
            raise Exception(message)

        return no_records == 1
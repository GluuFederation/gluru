import requests
import logging
from dateutil.relativedelta import relativedelta
from hashlib import sha1
import random

from smtplib import SMTPRecipientsRefused, SMTPException, SMTPConnectError, SMTPDataError, SMTPServerDisconnected, SMTPSenderRefused, SMTPAuthenticationError, SMTPResponseException

import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives

from django.template import loader

from django.utils import timezone
from django.utils.encoding import smart_bytes
from django.utils.six import text_type


requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('django')


def get_beginning_of_quarter(start_date):

    today = datetime.date.today()

    # fallback use first day of quarter we are currently in
    if not start_date or start_date > today:
        return datetime.date(today.year, today.month - (today.month - 1) % 3, 1)

    else:

        while start_date < today:
            beginning_of_quarter = start_date
            start_date = start_date + datetime.timedelta(days=91)

        return beginning_of_quarter


def format_minutes(minutes):
    if minutes < 0:
        return None
    if minutes < 60:
        return '{} minutes'.format(minutes)
    elif minutes == 60:
        return '1 hour'
    elif 60 <= minutes < 120:
        return '1 hour {} minutes'.format(minutes % 60)
    else:
        return '{} hours {} minutes'.format(minutes / 60, minutes % 60)


def format_timedelta(delta):

    if delta.days > 0:
        return '{} days'.format(delta.days)
    else:
        return '{} hours'.format(delta.seconds // 3600)


def get_base_url():

    site = Site.objects.get_current()

    return '{}://{}'.format(settings.PROTOCOL, site.domain)


def log_error(message):
    logger = logging.getLogger('django')
    logger.error(message)


def log_emails(message, level='INFO'):
    logger = logging.getLogger('emails')
    if level == 'ERROR':
        logger.error(message)
    else:
        logger.info(message)


def log_idp(message):
    logger = logging.getLogger('idp')
    logger.info(message)


def log_crm(message, level='INFO'):
    logger = logging.getLogger('crm')

    if level == 'ERROR':
        logger.error(message)

    else:
        logger.info(message)


def cstm_dates(d_start, d_end):

    s = dt.datetime.strptime('%s 00:00:01' % d_start, '%Y-%m-%d %H:%M:%S')
    f = dt.datetime.strptime('%s 23:59:59' % d_end, '%Y-%m-%d %H:%M:%S')

    return (s, f)

def get_fancy_time(d, display_full_version = False):
    """Returns a user friendly date format
    d: some datetime instace in the past
    display_second_unit: True/False
    """
    # some helpers lambda's
    plural = lambda x: 's' if x > 1 else ''
    singular = lambda x: x[:-1]
    # convert pluran (years) --> to singular (year)
    display_unit = lambda unit, name: '%s %s%s ago'%(unit, name, plural(unit)) if unit > 0 else ''

    # time units we are interested in descending order of significance
    tm_units = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

    rdelta = relativedelta(timezone.now(), d)   # capture the date difference
    for idx, tm_unit in enumerate(tm_units):
        first_unit_val = getattr(rdelta, tm_unit)
        if first_unit_val > 0:
            primary_unit = display_unit(first_unit_val, singular(tm_unit))
            if display_full_version and idx < len(tm_units) - 1:
                next_unit = tm_units[idx + 1]
                second_unit_val = getattr(rdelta, next_unit)
                if second_unit_val > 0:
                    secondary_unit = display_unit(second_unit_val, singular(next_unit))
                    return primary_unit + ', ' + secondary_unit
            return primary_unit
    return None

def send_email(subject_template_name, email_template_name, to_email,
              context=None, html_email_template_name=None,
              from_email=settings.DEFAULT_FROM_EMAIL, bcc=None):
    try:
        subject = loader.render_to_string(subject_template_name, context)
        body = loader.render_to_string(email_template_name, context)
        html = loader.render_to_string(html_email_template_name,context)
        if not isinstance(to_email, list):
            to_email = [to_email]
        if bcc and not isinstance(bcc, list):
            bcc = [bcc]
        if  settings.DEBUG and settings.LIVE_EMAIL:
            print requests.post(
            settings.MAILGUN_DOMAIN,
            auth=("api", settings.MAILGUN_KEY),
            data={"from": from_email,
                  "to":'your testing email',
                  "subject": subject,
                  "text": body
                  })
            print requests.post(
            settings.MAILGUN_DOMAIN,
            auth=("api", settings.MAILGUN_KEY),
            data={"from": from_email,
                  "to":'your testing email',
                  "subject": subject,
                  "html" : html
                  })
        else:
            print requests.post(
            settings.MAILGUN_DOMAIN,
            auth=("api", settings.MAILGUN_KEY),
            data={"from": from_email,
                  "to": to_email,
                  "bcc": bcc,
                  "subject": subject,
                  "text": body
                  })
            print requests.post(
            settings.MAILGUN_DOMAIN,
            auth=("api", settings.MAILGUN_KEY),
            data={"from": from_email,
                  "to": to_email,
                  "bcc": bcc,
                  "subject": subject,
                  "html" : html
                  })


    except SMTPRecipientsRefused as e:
        logger.error(e)


    except Exception as e:
        message = 'Failed to send email to {}, Subject: {}, Exception: {}'.format(
            to_email, subject_template_name, e)
        logger.exception(message)

def send_mail(subject_template_name, email_template_name, to_email,
              context=None, html_email_template_name=None,
              from_email=settings.DEFAULT_FROM_EMAIL, bcc=None):

    try:
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        if not isinstance(to_email, list):
            to_email = [to_email]

        if bcc and not isinstance(bcc, list):
            bcc = [bcc]

        if settings.DEBUG and settings.LIVE_EMAIL:
            email_message = EmailMultiAlternatives(subject, body, from_email, [settings.RECIPIENT_TEST_EMAIL])

        else:
            email_message = EmailMultiAlternatives(subject, body, from_email, to_email, bcc)

        if settings.TEST_TEXT_EMAIL:
            email_message.send()

        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    except SMTPException as e:
        logger.error(e)

    except SMTPServerDisconnected as e:
        logger.error(e)

    except SMTPResponseException as e:
        logger.error(e)

    except SMTPSenderRefused as e:
        logger.error(e)

    except SMTPDataError as e:
        logger.error(e)

    except SMTPConnectError as e:
        logger.error(e)

    except SMTPAuthenticationError as e:
        logger.error(e)

    except SMTPRecipientsRefused as e:
        logger.error(e)

    except Exception as e:
        message = 'Failed to send email to {}, Subject: {}, Exception: {}'.format(
            to_email, subject_template_name, e)
        logger.exception(message)


def generate_sha1(string, salt=None):

    if not isinstance(string, (str, text_type)):
        string = str(string)

    if not salt:
        salt = sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]

    salted_bytes = (smart_bytes(salt) + smart_bytes(string))
    hash_ = sha1(salted_bytes).hexdigest()

    return salt, hash_

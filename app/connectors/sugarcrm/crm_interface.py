import logging
from django.conf import settings
from django.db import connections

from profiles.constants import SUPPORT_PLANS
from profiles.models import create_or_get_company

import sugarcrm

import uuid

logger = logging.getLogger('crm')


def get_support_plan_by_account(account_name, get_date=False):
    """
    This functions provide support plan by company name.
    :param account_name: String Type(Company Name)
    :param get_date: Boolean Type(True or False)
    :return: list of String and Date(Basic,Standard,Premium,Enterprise,Partner and Plan Renewal Date)

    """
    return ["Basic"]


def account_inactive(account_name):
    """
    This function check that company is active or not.
    :param account_name: String Type(Company Name)
    :return:Boolean Type(True or False)
    """
    return False


def get_support_plan(user):
    """
    This function provide user support plan.
    :param user:String Type(user email)
    :return:Dictionary Type or String Type "{'support_plan':Basic or Standard or Premium or Enterprise , 'managed_service':True or False ,'start_date':Date ,'renewal_date':Date }"
    """
    return {'support_plan': 'Basic', 'managed_service': True, 'start_date': "N/A", 'renewal_date': "N/A"}


def get_contact(user):
    """
    This function provide user crm_id
    :param user: String Type
    :return: Varchar Type
    """
    return "abc123"


def get_partners():
    """
    This function provide list of partner companies.
    :return: List of strings
    """
    return []


def get_account_name_by_contact(contact_id):
    """
    This function provide company name.
    :param contact_id: Varchar Type(Crm_Id)
    :return: List Type(Company Name)
    """
    return "Company Name"

def sync_basic_user_with_crm(user):
    """
    Sync user detail with crm adjust this function according to your needs
    :param user:User Object
    :return:void
    """

def upgrade_user_record(user):
    """
    Upgrade user detail in crm adjust this function according to your needs
    :param user:User Object
    :return:void
    """



def downgrade_named_user(user):
    """
    Downgrade user detail in crm adjust this function according to your needs
    :param user:User Object
    :return:void
    """

def update_account_admin_status(user, downgrade=False):
    """
    Update user admin status in crm adjust this function according to your needs
    :param user:User Object , Downgrade = True or False
    :return:void
    """


def social_auth_sync_crm(is_new, user, *args, **kwargs):

    """
    This function authenticate and sync users.
    :param is_new: True or False
    :param user: User Object
    :param args:
    :param kwargs:
    :return: void
    """


def get_account_id_by_name(account_name):
    """
    This function provide company id
    :param account_name: String Type
    :return: Varchar Type
    """
    return "123abc"




def add_partnership(partnership):
    """
    This function add partnership in crm
    :param partnership: Partnership object
    :return: void
    """

def remove_partnership(partnership):
    """
    This function remove partnership in crm
    :param partnership: Partnership object
    :return: void
    """

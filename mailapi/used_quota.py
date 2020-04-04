from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm.exc import NoResultFound

from .domain import domain_exists
from .password import generate_md5_password
from .maildir import generate_maildir_path
from .models import Mailbox, UsedQuota
from .helpers import parse_email_domain
from .alias import add_alias, delete_aliases, delete_alias
from .mailbox import mailbox_exists
from .db import get_db_session
from .exc import NoSuchDomain, MailboxExists, NoSuchMailbox


def get_domain_sum_used_quota(domain: str):
    if not domain_exists(domain):
        raise NoSuchDomain(domain)

    return get_db_session().query(
        func.sum(UsedQuota.bytes).label('bytes'), func.sum(UsedQuota.messages).label('messages'),
    ).filter_by(domain=domain).one()


def get_mailbox_sum_used_quota(email_address: str):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)

    return get_db_session().query(
        UsedQuota.bytes, UsedQuota.messages
    ).filter_by(username=email_address).one()


def get_domain_used_quota(domain: str):
    if not domain_exists(domain):
        raise NoSuchDomain(domain)
    return get_db_session().query(UsedQuota).filter_by(domain=domain).all()


def get_mailbox_used_quota(email_address: str):
    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)
    return get_db_session().query(UsedQuota).filter_by(username=email_address).one()


def delete_used_quota_mailbox(email_address):
    """ Deletes the mailbox from the database by the given email address.

    :param email_address: String
    :return: True if success else False
    """

    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)

    num_deleted = get_db_session().query(UsedQuota).filter_by(username=email_address).delete()

    return num_deleted == 1


def reset_mailbox_used_quota(email_address):
    """ Sets the password for the given email address to the given password

    :param email_address: Email address
    :param plain_password: The new desired password in plain text form
    :return: True if success
    :raises NoSuchMailbox: If the given email address does not exist
    """

    if not mailbox_exists(email_address):
        raise NoSuchMailbox(email_address)

    used_quota = get_mailbox_used_quota(email_address)
    used_quota.bytes = 0
    used_quota.messages = 0

    db_session = get_db_session()
    db_session.add(used_quota)
    db_session.flush()

    return True

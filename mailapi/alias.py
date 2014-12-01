from sqlalchemy.exc import IntegrityError

from .models import Alias
from .helpers import parse_email_domain
from .db import get_db_session
from .validators import is_email


def add_alias(source, dest):
    """ Create an alias for the given email address

    :param source: Incoming email address
    :param dest: Redirect to this mailbox
    :return: Alias
    :raises ValueError: if an invalid source or dest email address is provided
    :raises RuntimeError: if the given alias already exists
    """

    if not is_email(source):
        raise ValueError('Invalid source email address provided: %s' % source)

    if not is_email(dest):
        raise ValueError('Invalid destination email address provided: %s' %
                         dest)

    local_part, domain = parse_email_domain(dest)

    alias = Alias()
    alias.address = source
    alias.goto = dest
    alias.domain = domain

    db_session = get_db_session()
    try:
        db_session.add(alias)
        db_session.flush()
        return alias
    except IntegrityError:
        db_session.rollback()
        raise RuntimeError('The given alias (%s --> %s) already exists.' %
                           (source, dest))


def get_aliases(dest):
    """ Get all aliases that redirect to the given @dest email address

    :param email_address: String
    :return: List of mailapi.models.Alias objects
    """

    return get_db_session().query(Alias).filter_by(goto=dest).all()


def delete_aliases(dest):
    """ Deletes all aliases that redirect to the given email address except for
    the self-referrential alias which must be explicitly deleted.

    :param dest: The goto address
    :return: True if success else False
    """

    db_session = get_db_session()
    num_deleted = db_session.query(Alias).\
        filter(Alias.goto == dest).\
        filter(Alias.address != dest).\
        delete()
    db_session.flush()

    return num_deleted >= 1


def delete_alias(source, dest):
    """ Delete an alias matching the given @source and @dest addresses

    :param source: String
    :param dest: String
    :return: True if success
    """

    db_session = get_db_session()
    num_deleted = db_session.query(Alias).\
        filter(Alias.address == source,
               Alias.goto == dest).\
        delete()
    db_session.flush()

    return num_deleted == 1

from sqlalchemy.orm.exc import NoResultFound
from .models import Domain, Mailbox, Alias
from .db import get_db_session
from .validators import is_domain


# Error messages can go here
DOMAIN_DNE = '''The given domain does not exist: %s'''


def create_domain(domain_name, description=''):
    """ Adds domain name to the database

    :param domain_name: A valid domain name
    :param description: A description of the domain
    :return: Domain model object
    :raises RuntimeError: if the given domain already exists
    :raises ValueError: if the domain name is not a domain name
    """

    if not is_domain(domain_name):
        raise ValueError('Invalid domain name supplied: %s' % domain_name)

    if domain_exists(domain_name):
        raise RuntimeError

    db_session = get_db_session()
    d = Domain(domain=domain_name, description=description)
    db_session.add(d)
    db_session.flush()
    return d


def get_domain(domain_name):
    """ Gets a domain with the given name from the db

    :param domain_name: String
    :return: Domain or None
    """

    try:
        domain = get_db_session().query(Domain).\
            filter_by(domain=domain_name).one()
        return domain
    except NoResultFound:
        return None


def get_all_mailboxes(domain_name):
    """ Gets a list of all mailboxes associated with the given domain

    :param domain_name: String
    :return: Listof Mailbox objects
    """

    if not domain_exists(domain_name):
        raise RuntimeError(DOMAIN_DNE % domain_name)

    return get_db_session().query(Mailbox).filter_by(domain=domain_name).all()


def get_all_domains():
    """ Fetches all domains from the database

    :return: List of domains
    """

    domains = get_db_session().query(Domain).all()
    return domains


def delete_domain(domain_name):
    """ Deletes the given domain name from the database

    :param domain_name: String
    :return: True if success
    :raises RuntimeError: if hte given domain name doesn't exist
    """

    if not domain_exists(domain_name):
        raise RuntimeError(DOMAIN_DNE % domain_name)

    # Delete aliases and mailboxes
    delete_aliases(domain_name)
    delete_mailboxes(domain_name)

    db_session = get_db_session()
    num_deleted = db_session.query(Domain).\
        filter_by(domain=domain_name).delete()
    db_session.flush()

    return num_deleted == 1


def delete_aliases(domain_name):
    """ Deletes all aliases in the given domain

    :param domain_name: String
    :return: True if success else False
    :raises RuntimeError: If the given domain does not exist
    """

    if not domain_exists(domain_name):
        raise RuntimeError(DOMAIN_DNE % domain_name)

    num_deleted = get_db_session().query(Alias).\
        filter_by(domain=domain_name).delete()

    return num_deleted >= 1


def delete_mailboxes(domain_name):
    """ Deletes all mailboxes (and their aliases) in the given domain

    :param domain_name: String
    :return: True if success else False
    :raises RuntimeError: If the given domain does not exist
    """

    if not domain_exists(domain_name):
        raise RuntimeError(DOMAIN_DNE % domain_name)

    num_deleted = get_db_session().query(Mailbox).\
        filter_by(domain=domain_name).delete()

    return num_deleted >= 1


def domain_exists(domain_name):
    """ Checks if the given domain name exists in the database

    :param domain_name: String
    :return: True if domain exists else False
    """

    try:
        get_db_session().query(Domain).filter_by(domain=domain_name).one()
        return True
    except NoResultFound:
        return False

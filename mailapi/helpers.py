import random
from .validators import is_email


def parse_email_domain(address):
    """ Returns a 2-tuple in the form of (local part, domain)

    For info on nomenclature see:
                    http://en.wikipedia.org/wiki/Email_address#Syntax

    :param address: String
    :return: (local_part, domain)
    :raises: ValueError if an invalid email address is given
    """

    if not is_email(address):
        raise ValueError('Invalid email address provided: %s' % address)

    local_part, domain = address.split('@')

    return local_part, domain


def generate_random_strings(length=10):
    """Create a random password of specified

    Source: https://bitbucket.org/zhb/iredadmin-ose/src/fb7d39f487feb4b2eb2635990f1363ba73e404e6/libs/iredutils.py?at=default#cl-291 # noqa (suppresses PEP8 warning)

    Modified to be PEP8 compliant
    """

    try:
        length = int(length) or 10
    except ValueError:
        length = 10

    # Characters used to generate the random password
    chars = '23456789' + 'abcdefghjkmnpqrstuvwxyz' + '23456789' + \
            'ABCDEFGHJKLMNPQRSTUVWXYZ' + '23456789'

    return ''.join(random.choice(chars) for x in range(length))

""" Validation helper functions

Source: https://bitbucket.org/zhb/iredadmin-ose/src/fb7d39f487feb4b2eb2635990f1363ba73e404e6/libs/iredutils.py?at=default # noqa

Modified to be PEP8 compliant
"""
import re

# Email.
email_re = r'''[\w\-][\w\-\.]*@[\w\-][\w\-\.]+[a-zA-Z]{2,15}'''

# Domain.
domain_re = r'''[\w\-][\w\-\.]*\.[a-z]{2,15}'''

INVALID_EMAIL_CHARS = '~!#$%^&*()\\/\ '
INVALID_DOMAIN_CHARS = '~!#$%^&*()+\\/\ '


def is_email(s):
    s = str(s)
    if len(set(s) & set(INVALID_EMAIL_CHARS)) > 0 \
       or '.' not in s \
       or s.count('@') != 1:
        return False

    re_comp_email = re.compile(email_re + '$', re.IGNORECASE)
    if re_comp_email.match(s):
        return True
    else:
        return False


def is_domain(s):
    s = str(s)
    if len(set(s) & set(INVALID_DOMAIN_CHARS)) > 0 or '.' not in s:
        return False

    re_comp_domain = re.compile(domain_re + '$', re.IGNORECASE)
    if re_comp_domain.match(s):
        return True
    else:
        return False


def is_strict_ip(s):
    s = str(s)
    fields = s.split('.')
    if len(fields) != 4:
        return False

    # Must be an interger number (0 < number < 255)
    for fld in fields:
        if fld.isdigit():
            if not 0 < int(fld) < 255:
                return False
        else:
            return False

    return True

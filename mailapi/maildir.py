import time

from .validators import is_email


def generate_maildir_path(mail,
                          hashed_maildir=True,
                          prepend_domain_name=True,
                          append_timestamp=True):
    """ Generate path of mailbox.

    Source: https://bitbucket.org/zhb/iredadmin-ose/src/fb7d39f487feb4b2eb2635990f1363ba73e404e6/libs/iredutils.py?at=default#cl-544

    Modified to raise a ValueError instead of returning a tuple

    :raises ValueError: If the email address is invalid.
    """

    if not is_email(mail):
        raise ValueError('Invalid email address.')

    # Get user/domain part from mail address.
    username, domain = mail.split('@', 1)

    # Get current timestamp.
    timestamp = ''
    if append_timestamp:
        timestamp = time.strftime('-%Y.%m.%d.%H.%M.%S')

    if hashed_maildir is True:
        if len(username) >= 3:
            maildir = "%s/%s/%s/%s%s/" % (
                username[0], username[1], username[2], username, timestamp,
            )
        elif len(username) == 2:
            maildir = "%s/%s/%s/%s%s/" % (
                username[0], username[1], username[1], username, timestamp,
            )
        else:
            maildir = "%s/%s/%s/%s%s/" % (
                username[0], username[0], username[0], username, timestamp,
            )

        mail_message_store = maildir
    else:
        mail_message_store = "%s%s/" % (username, timestamp,)

    if prepend_domain_name:
        mail_message_store = domain + '/' + mail_message_store

    return mail_message_store.lower()

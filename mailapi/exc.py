""" Exception class definitions go here.
"""


class NoSuchDomain(Exception):
    """ Domain does not exist
    """
    def __init__(self, domain_name):
        error_message = 'The domain %s does not exist.' % domain_name
        super(NoSuchDomain, self).__init__(error_message)


class DomainExists(Exception):
    """ The given domain already exists in the database
    """
    def __init__(self, domain_name):
        error_message = 'The domain %s already exists.' % domain_name
        super(DomainExists, self).__init__(error_message)


class NoSuchMailbox(Exception):
    """ The mailbox does not exist in the database
    """
    def __init__(self, email_address):
        error_message = 'A mailbox with the email address %s does not ' \
                        'exist.' % email_address
        super(NoSuchMailbox, self).__init__(error_message)


class MailboxExists(Exception):
    """ Mailbox duplicate exception
    """
    def __init__(self, email_address):
        error_message = 'A mailbox with the email address %s already exists.' \
                        % email_address
        super(MailboxExists, self).__init__(error_message)


class DbInitError(Exception):
    """ To be raised when the database connection hasn't been initialized
    """
    pass


class AliasExists(Exception):
    """ The given alias exists in the database
    """
    def __init__(self, source, dest):
        error_message = 'The given alias (%s --> %s) already exists.' % \
                        (source, dest)

        super(AliasExists, self).__init__(error_message)

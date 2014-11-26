""" Exception class definitions go here.
"""


class DomainDNE(Exception):
    """ Domain does not exist
    """
    pass


class MailBoxExists(Exception):
    """ Mailbox duplicate exception
    """
    pass

from unittest import TestCase

from ..mailbox import (
    create_mailbox,
    delete_mailbox,
    mailbox_exists,
    get_all_mailboxes,
    get_mailbox,
)
from ..domain import create_domain, delete_domain
from ..models import Mailbox


class MailboxBaseCase(TestCase):
    def setUp(self):
        self.domain_name = 'testdomain.lan'
        self.domain = create_domain(self.domain_name, 'A Test Domain')

    def tearDown(self):
        delete_domain(self.domain_name)


class CreateMailboxTests(MailboxBaseCase):
    def test_create_mailbox(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Result should be a mailbox object
        self.assertIsInstance(mailbox, Mailbox)

        # Should be able to delete the mailbox
        self.assertTrue(delete_mailbox(email_address))

    def test_create_mailbox_invalid_address(self):
        # Should raise a value error cause it can't parse the email address
        self.assertRaises(ValueError,
                          create_mailbox,
                          'asdlkfjaslkdjfalksdjf',
                          'Test User',
                          'password123')

    def test_create_mailbox_that_exists(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        create_mailbox(email_address, 'Test User', 'password123')

        # creating the same mailbox should raise a RuntimeError
        self.assertRaises(RuntimeError,
                          create_mailbox,
                          email_address,
                          'Test User',
                          'password123')

        # Should be able to delete the mailbox
        self.assertTrue(delete_mailbox(email_address))

    def test_create_mailbox_for_domain_that_doesnt_exist(self):
        self.assertRaises(RuntimeError,
                          create_mailbox,
                          'test@fakedomain.tld',
                          'Test User',
                          'password123')


class MailboxExistsTests(MailboxBaseCase):
    def test_mailbox_exists(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # Creates the mailbox
        create_mailbox(email_address, 'Test User', 'password123')

        # The mailbox we just created should exist
        self.assertTrue(mailbox_exists(email_address))

        # Deletes the mailbox
        self.assertTrue(delete_mailbox(email_address))

        # Now that we deleted the mailbox, it should exist, right?
        self.assertFalse(mailbox_exists(email_address))


class DeleteMailboxTests(MailboxBaseCase):
    def test_delete_mailbox(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # Creates the mailbox
        create_mailbox(email_address, 'Test User', 'password123')

        # The mailbox we just created should exist
        self.assertTrue(mailbox_exists(email_address))

        # Deletes the mailbox
        self.assertTrue(delete_mailbox(email_address))

        # Now that we deleted the mailbox, it should exist, right?
        self.assertFalse(mailbox_exists(email_address))

    def test_delete_invalid_mailbox(self):
        email_address = ''.join(['asdfasdflksdf', '@', self.domain_name])
        self.assertRaises(RuntimeError, delete_mailbox, email_address)


class GetMailboxTests(MailboxBaseCase):
    def test_get_mailbox(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # Creates a mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # We should get back the mailbox we just created
        self.assertEqual(get_mailbox(email_address), mailbox)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

    def test_get_nonexistant_mailbox(self):
        self.assertFalse(get_mailbox('asjdhfakjsdhf'))

    def test_get_all_mailboxes(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # Creates a mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Gets a list of all mailboxes
        mailboxes = get_all_mailboxes()

        # It should be a list
        self.assertIsInstance(mailboxes, list)

        # Our mailbox should be in it
        self.assertIn(mailbox, mailboxes)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

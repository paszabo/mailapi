from unittest import TestCase
from datetime import datetime

from ..mailbox import (
    create_mailbox,
    delete_mailbox,
    mailbox_exists,
    get_all_mailboxes,
    get_mailbox,
    reset_mailbox_password,
    search_mailboxes,
)
from ..alias import get_aliases
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

    def test_mailbox_created_and_updated_dates_are_populated(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Makes sure the created and updated fields are datetimes
        self.assertIsInstance(mailbox.created, datetime)
        self.assertIsInstance(mailbox.modified, datetime)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))


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

    def test_alias_deleted(self):
        """ Makes sure that the self referrential alias gets deleted """

        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        create_mailbox(email_address, 'Test User', 'password123')

        # Gets the list of aliases associated with this email address
        aliases = get_aliases(email_address)

        # The self-referrential alias should be the only alias created
        selfref_alias = aliases[0]
        self.assertEqual(selfref_alias.address, email_address)
        self.assertEqual(selfref_alias.goto, email_address)

        # Deletes the mailbox
        self.assertTrue(delete_mailbox(email_address))

        # There should be no aliases associated with the email address now
        self.assertEqual(len(get_aliases(email_address)), 0)


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


class MailboxPasswordResetTests(MailboxBaseCase):
    def test_reset_password(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        create_mailbox(email_address, 'Test User', 'password123')

        # True implies the mailbox was updated with the new password
        self.assertTrue(reset_mailbox_password(email_address,
                                               'password90125'))

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

    def test_reset_password_for_nonexistant_mailbox(self):
        # A RuntimeError should be raised when resetting the password for a
        # non existant mailbox
        self.assertRaises(RuntimeError,
                          reset_mailbox_password,
                          'adsfadsf',
                          'new password')

    def test_modified_date_updated_after_pw_reset(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Stores the initial modified dttm
        init_mod_dttm = mailbox.modified

        # True implies the mailbox was updated with the new password
        self.assertTrue(reset_mailbox_password(email_address,
                                               'password90125'))

        # Refresh the mailbox
        mailbox = get_mailbox(email_address)

        # Now that the password was reset, the modified date should be updated
        self.assertGreater(mailbox.modified, init_mod_dttm)

        # The password changed field should be populated now
        self.assertIsInstance(mailbox.passwordlastchanged, datetime)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))


class MailboxSearchTest(MailboxBaseCase):
    def test_mailbox_search(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Searches for our mailbox
        search_results = search_mailboxes('testusr')

        # The result should be a list
        self.assertIsInstance(search_results, list)

        # Our mailbox should be in the results
        self.assertIn(mailbox, search_results)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

    def test_search_mailbox_by_domain(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Searches for our mailbox
        search_results = search_mailboxes(self.domain_name)

        # The result should be a list
        self.assertIsInstance(search_results, list)

        # Our mailbox should be in the results
        self.assertIn(mailbox, search_results)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

    def test_search_mailbox_by_name(self):
        email_address = ''.join(['testusr', '@', self.domain_name])

        # creates the mailbox
        mailbox = create_mailbox(email_address, 'Test User', 'password123')

        # Searches for our mailbox
        search_results = search_mailboxes('Test User')

        # The result should be a list
        self.assertIsInstance(search_results, list)

        # Our mailbox should be in the results
        self.assertIn(mailbox, search_results)

        # cleanup
        self.assertTrue(delete_mailbox(email_address))

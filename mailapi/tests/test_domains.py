from unittest import TestCase

from ..models import Domain
from ..domain import (
    create_domain,
    delete_domain,
    get_all_domains,
    get_domain,
    domain_exists,
    delete_mailboxes,
    delete_aliases,
    get_all_mailboxes,
)
from ..mailbox import create_mailbox
from ..exc import DomainExists, NoSuchDomain


class CreateDomainTests(TestCase):
    def test_create_domain(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        # Creates a domain
        domain = create_domain(domain_name, domain_description)

        # Result should be a domain model object
        self.assertIsInstance(domain, Domain)

        # Make sure the fields match
        self.assertEqual(domain.domain, domain_name)
        self.assertEqual(domain.description, domain_description)

        # Make sure we can delete
        self.assertTrue(delete_domain(domain_name))

    def test_create_existing_domain(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        # Creates the domain
        create_domain(domain_name, domain_description)

        # Creating the same domain again should raise a DomainExists exception
        self.assertRaises(DomainExists,
                          create_domain,
                          domain_name,
                          domain_description)

        # Make sure we can delete
        self.assertTrue(delete_domain(domain_name))

    def test_create_domain_with_invalid_domain_name(self):
        # Creating a domain with an invalid domain name should
        # raise a ValueError
        self.assertRaises(ValueError,
                          create_domain,
                          'notadomainname',
                          'Not a domain name')


class GetDomainTests(TestCase):
    def test_get_domain(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        domain = create_domain(domain_name, domain_description)

        # Should get back the domain we created
        self.assertEqual(domain, get_domain(domain_name))

        # cleanup
        self.assertTrue(delete_domain(domain_name))

    def test_get_nonexistant_domain(self):
        # We should get None as opposed to any kind of exception
        # My Question: is this ideal?
        self.assertIsNone(get_domain('asdlkjdfasldkjfal'))

    def test_get_all_domains(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        # Makes sure at least one domain is defined
        create_domain(domain_name, domain_description)

        # We should get a list back
        self.assertIsInstance(get_all_domains(), list)

        # Since we create a domain, the list should be at least 1 element long
        self.assertGreaterEqual(len(get_all_domains()), 1)

        # cleanup
        self.assertTrue(delete_domain(domain_name))


class DeleteDomainTests(TestCase):
    def test_delete_nonexistant_domain(self):
        # Deleting a non-existant domain should raise a NoSuchDomain error
        self.assertRaises(NoSuchDomain, delete_domain, 'aslkdjhfaksjdhfakj')


class DeleteDomainAliasesTests(TestCase):
    def test_delete_aliases(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        create_domain(domain_name, domain_description)

        # Creates a mailbox so there is an alias to be deleted
        create_mailbox('test_user@testdomain.lan',
                       'Test User',
                       'password123',
                       100)

        # True implies at least one alias was deleted
        self.assertTrue(delete_aliases(domain_name))

        # cleanup
        self.assertTrue(delete_domain(domain_name))

    def test_delete_aliases_for_nonexistant_domain(self):
        self.assertRaises(NoSuchDomain, delete_aliases, 'asdfasdfasdf')

    def test_delete_aliases_for_zeroalias_domain(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        create_domain(domain_name, domain_description)

        # Since no aliases were created, the result of deleting all aliases
        # in this domain should be False.
        self.assertFalse(delete_aliases(domain_name))

        # cleanup
        self.assertTrue(delete_domain(domain_name))


class DeleteDomainMailboxesTests(TestCase):
    def test_delete_mailboxes(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        create_domain(domain_name, domain_description)

        # Creates a mailbox so there is a mailbox to delete
        create_mailbox('test_user@testdomain.lan',
                       'Test User',
                       'password123')

        # True implies that at least one mailbox was deleted
        self.assertTrue(delete_mailboxes(domain_name))

        # cleanup
        self.assertTrue(delete_domain(domain_name))

    def test_delete_mailboxes_for_nonexistant_domain(self):
        self.assertRaises(NoSuchDomain, delete_mailboxes, 'asdfasdf')

    def test_delete_mailboxes_for_zeromailbox_domain(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        # Creates the domain
        create_domain(domain_name, domain_description)

        # Since no mailboxes were created, the result of deleting all the
        # mailboxes in the domain should be False.
        self.assertFalse(delete_mailboxes(domain_name))

        # cleanup
        self.assertTrue(delete_domain(domain_name))


class DomainExistsTests(TestCase):
    def test_domain_exists(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        create_domain(domain_name, domain_description)

        # We created it so it must exist
        self.assertTrue(domain_exists(domain_name))

        # Deletes the domain
        self.assertTrue(delete_domain(domain_name))

        # Now it shouldn't exist, right?
        self.assertFalse(domain_exists(domain_name))


class GetAllMailboxesTests(TestCase):
    def test_get_all_mailboxes(self):
        domain_name = 'testdomain.lan'
        domain_description = 'Test Domain'

        # Creates a domain
        create_domain(domain_name, domain_description)

        # Create a mailbox in the domain
        mailbox = create_mailbox('testuser@testdomain.lan',
                                 'Test User',
                                 'password123')

        # Gets all the mailboxes associated with the domain
        mailboxes = get_all_mailboxes(domain_name)

        # The result should be a list
        self.assertIsInstance(mailboxes, list)

        # Our mailbox should be in the list we got back
        self.assertIn(mailbox, mailboxes)

        # cleanup (also deletes the mailbox)
        self.assertTrue(delete_domain(domain_name))

    def test_get_all_mailboxes_for_nonexistant_domain(self):
        # Should raise a NoSuchDomain error
        self.assertRaises(NoSuchDomain, get_all_mailboxes, 'asdfkljahsdfkja')

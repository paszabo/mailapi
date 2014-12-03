from unittest import TestCase

from ..models import Alias
from ..alias import add_alias, delete_alias, delete_aliases, get_aliases
from ..domain import create_domain, delete_domain
from ..mailbox import create_mailbox
from ..exc import AliasExists


class AliasBaseCase(TestCase):
    def setUp(self):
        # Creates a domain
        self.domain_name = 'testdomain.lan'
        self.domain = create_domain(self.domain_name, 'Test Domain')

        # Creates a mailbox
        self.email_address = 'testuser@testdomain.lan'
        self.mailbox = create_mailbox(self.email_address,
                                      'Test User',
                                      'password1234')

    def tearDown(self):
        # Deleting the domain deletes the mailbox
        delete_domain(self.domain.domain)


class AddAliasTests(AliasBaseCase):
    def test_add_alias(self):
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = self.email_address

        # Adds the alias to the DB
        alias = add_alias(alias_source, alias_dest)

        # The result is an Alias object
        self.assertIsInstance(alias, Alias)

        # Deletion should be a success
        self.assertTrue(delete_alias(alias_source, alias_dest))

    def test_add_alias_with_invalid_source_email_address(self):
        alias_source = 'asdfasdf'
        alias_dest = self.email_address

        self.assertRaises(ValueError,
                          add_alias,
                          alias_source,
                          alias_dest)

    def test_add_alias_with_invalid_dest_email_address(self):
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = 'aslkdfjalsdf'

        self.assertRaises(ValueError,
                          add_alias,
                          alias_source,
                          alias_dest)

    def test_add_duplicate_alias(self):
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = self.email_address

        # Adds the alias to the DB
        add_alias(alias_source, alias_dest)

        # Adding the same alias should raise a AliasExists exception
        self.assertRaises(AliasExists, add_alias, alias_source, alias_dest)

        # cleanup
        self.assertTrue(delete_alias(alias_source, alias_dest))


class GetAliasTests(AliasBaseCase):
    def test_get_aliases(self):
        # Creates an alias
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = self.email_address

        # Adds the alias
        add_alias(alias_source, alias_dest)

        # Gets all the aliases associated with the given email address
        aliases = get_aliases(alias_dest)

        # The result should be a list
        self.assertIsInstance(aliases, list)

        # Mailboxes have a alias pointing to itself plus the one we just
        # created == 2
        self.assertEquals(len(aliases), 2)

        # cleanup
        self.assertTrue(delete_alias(alias_source,
                                     alias_dest))

    def test_get_aliases_for_nonexistant_dest(self):
        aliases = get_aliases('asdasdfasdf')

        # Should still get a list back...
        self.assertIsInstance(aliases, list)

        # ...but it should have length 0
        self.assertEqual(len(aliases), 0)


class DeleteAliasTests(AliasBaseCase):
    def test_delete_aliases(self):
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = self.email_address

        # Adds an alias
        add_alias(alias_source, alias_dest)

        # True implies that at least one alias was delete
        self.assertTrue(delete_aliases(alias_dest))

        # However, the self-refferential alias should remain
        # and (must be explicitly delete)
        self.assertEqual(len(get_aliases(alias_dest)), 1)

    def test_delete_aliases_for_nonexistant_dest(self):
        # False implies 0 aliases were deleted
        self.assertFalse(delete_aliases('asdfasdfasd'))

    def test_delete_single_alias(self):
        alias_source = ''.join(['testuser_alias', '@', self.domain_name])
        alias_dest = self.email_address

        # Adds an alias
        add_alias(alias_source, alias_dest)

        # True implies that at least one alias was delete
        self.assertTrue(delete_alias(alias_source, alias_dest))

    def test_delete_single_nonexistant_alias(self):
        # Should be false as nothing was delete
        self.assertFalse(delete_alias('fake_source', 'fake_dest'))

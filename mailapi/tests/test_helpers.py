from unittest import TestCase

from ..helpers import parse_email_domain


class ParseEmailTest(TestCase):
    def test_valid_email(self):
        email_address = 'testuser@testdomain.lan'

        local_part, domain = parse_email_domain(email_address)

        self.assertEqual(local_part, 'testuser')
        self.assertEqual(domain, 'testdomain.lan')

    def test_invalid_email(self):
        invalid_email_address = 'lol not an email address at all'

        self.assertRaises(ValueError,
                          parse_email_domain,
                          invalid_email_address)

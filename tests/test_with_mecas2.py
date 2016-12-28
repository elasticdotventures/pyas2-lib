from __future__ import unicode_literals, absolute_import, print_function
from .context import as2
import unittest
import os

TEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testdata')


class TestMecAS2(unittest.TestCase):

    def setUp(self):
        self.test_file = open(
                os.path.join(TEST_DIR, 'payload.txt'))

        self.org = as2.Organization(
            as2_id='some_organization',
            sign_key=os.path.join(TEST_DIR, 'cert_test_private.pem'),
            sign_key_pass='test',
            decrypt_key=os.path.join(TEST_DIR, 'cert_test_private.pem'),
            decrypt_key_pass='test'
        )
        self.partner = as2.Partner(
            as2_id='mecas2',
            verify_cert=os.path.join(TEST_DIR, 'cert_mecas2_public.pem'),
            encrypt_cert=os.path.join(TEST_DIR, 'cert_mecas2_public.pem'),
            indefinite_length=True
        )

    def tearDown(self):
        self.test_file.close()

    def test_compressed_message(self):
        """ Test Compressed Message received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        test_file = os.path.join(TEST_DIR, 'mecas2_compressed.as2')
        with open(test_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.compress)
        self.assertEqual(
            self.test_file.read(), in_message.payload.get_payload())

    def test_encrypted_message(self):
        """ Test Encrypted Message received from Mendelson AS2"""

        # Parse the generated AS2 message as the partner
        test_file = os.path.join(TEST_DIR, 'mecas2_encrypted.as2')
        with open(test_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypt)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertEqual(
            self.test_file.read(), in_message.payload.get_payload())

    def test_signed_message(self):
        """ Test Unencrypted Signed Uncompressed Message """
        # Parse the generated AS2 message as the partner
        test_file = os.path.join(TEST_DIR, 'mecas2_signed.as2')
        with open(test_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.sign)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(
            self.test_file.read(), in_message.payload.get_payload())

    def test_encrypted_signed_message(self):
        """ Test Encrypted Signed Uncompressed Message """

        # Parse the generated AS2 message as the partner
        test_file = os.path.join(TEST_DIR, 'mecas2_signed_encrypted.as2')
        with open(test_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypt)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertTrue(in_message.sign)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(
            self.test_file.read(), in_message.payload.get_payload())

    def test_encrypted_signed_compressed_message(self):
        """ Test Encrypted Signed Compressed Message """

        # Parse the generated AS2 message as the partner
        test_file = os.path.join(
            TEST_DIR, 'mecas2_compressed_signed_encrypted.as2')
        with open(test_file, 'rb') as fp:
            in_message = as2.Message()
            in_message.parse(
                fp.read(),
                find_org_cb=self.find_org,
                find_partner_cb=self.find_partner
            )

        # Compare the mic contents of the input and output messages
        self.assertTrue(in_message.encrypt)
        self.assertEqual(in_message.enc_alg, 'tripledes_192_cbc')
        self.assertTrue(in_message.sign)
        self.assertEqual(in_message.digest_alg, 'sha1')
        self.assertEqual(
            self.test_file.read(), in_message.payload.get_payload())

    def find_org(self, headers):
        return self.org

    def find_partner(self, headers):
        return self.partner

from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import CredentialInterface
from src.models.db_models.user import Credentials, User


class CredentialInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.user_1 = User(
            name='testName',
            last_name='testLastName',
            email='test1@test.com'
        )
        self.user_1.save()
        self.user_2 = User(
            name='testAnotherName',
            last_name='testLastName',
            email='test2@test.com'
        )
        self.user_2.save()

        Credentials(
            user=self.user_1,
            password='123456789',
            security_code='318273',
            otp_code='d+qsp92md2q22h1lnf0dm2'
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        result = CredentialInterface.find_one(self.user_1)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Credentials)
        self.assertEqual(result.user.email, 'test1@test.com')

    def test_find_one_not_found(self):
        result = CredentialInterface.find_one(self.user_2)

        self.assertIsNone(result)

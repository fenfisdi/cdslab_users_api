from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import UserInterface
from src.models.db_models.user import User


class UserInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        User(
            name='testName',
            last_name='testLastName',
            email='test@test.com'
        ).save()
        User(
            name='testName',
            email='test2@test.com',
            is_active=True
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        user = UserInterface.find_one('test@test.com')

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@test.com')

    def test_find_one_not_found(self):
        user = UserInterface.find_one('test1@test.com')

        self.assertIsNone(user)

    def test_find_one_active_successful(self):
        user = UserInterface.find_one_active('test2@test.com')

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test2@test.com')

    def test_find_one_active_not_found(self):
        user = UserInterface.find_one_active('test@test.com')

        self.assertIsNone(user)

    def test_find_one_inactive_successful(self):
        user = UserInterface.find_one_inactive('test@test.com')

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@test.com')

    def test_find_one_inactive_not_found(self):
        user = UserInterface.find_one_inactive('test2@test.com')

        self.assertIsNone(user)

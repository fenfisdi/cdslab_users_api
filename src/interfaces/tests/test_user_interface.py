from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import UserInterface
from src.models.db_models.user import User


class UserInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

        self.inactive_user = 'test@test.com'
        User(
            name='testName',
            last_name='testLastName',
            email=self.inactive_user
        ).save()

        self.active_user = 'test2@test.com'
        User(
            name='testName',
            email=self.active_user,
            is_valid=True
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        user = UserInterface.find_one(self.active_user)

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.active_user)

    def test_find_one_not_found(self):
        user = UserInterface.find_one('test1@test.com')

        self.assertIsNone(user)

    def test_find_one_active_successful(self):
        user = UserInterface.find_one(self.active_user)

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.active_user)

    def test_find_one_active_not_found(self):
        user = UserInterface.find_one(self.inactive_user)

        self.assertIsNone(user)

    def test_find_one_inactive_successful(self):
        user = UserInterface.find_one(self.inactive_user, is_valid=False)

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.inactive_user)

    def test_find_one_inactive_not_found(self):
        user = UserInterface.find_one(self.active_user, is_valid=False)

        self.assertIsNone(user)

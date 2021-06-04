from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = 'src.routes.user'
    return ".".join([source, path])


class CreateUserRouteTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            name='name',
            last_name='last name',
            phone='1823725629',
            phone_prefix='+57',
            institution='university',
            institution_role='student',
            birthday='2001-03-20',
            email='test@test.com',
            role='user',
            password='a1b2c3d4',
            otp_code='z9y8x7',
            security_questions=[]
        )
        self.route = '/user'

    @patch(solve_path('SecurityQuestions'))
    @patch(solve_path('Credentials'))
    @patch(solve_path('User'))
    @patch(solve_path('UserInterface'))
    def test_create_user_successful(
            self,
            user_interface: Mock,
            user: Mock,
            credential: Mock,
            questions: Mock
     ):
        user_interface.find_one.return_value = None
        user.return_value = Mock(
            save=Mock(return_value={}),
            to_mongo=Mock(return_value={})

        )
        credential.return_value = Mock(save=Mock(return_value={}))
        questions.return_value = Mock(save=Mock(return_value={}))

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 201)

    @patch(solve_path('UserInterface'))
    def test_create_user_exist(
            self,
            user_interface: Mock,
     ):
        user_interface.find_one.return_value = Mock()

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class ValidateUserRouteTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test2@test.com/validate'

    @patch(solve_path('UserInterface'))
    def test_validate_user_successful(self, user_interface: Mock):
        user_interface.find_one.return_value = Mock()

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_validate_user_not_found(self, user_interface: Mock):
        user_interface.find_one.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


class FindUserRouteTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test3@test.com'

    @patch(solve_path('UserInterface'))
    def test_find_user_successful(self, user_interface: Mock):
        user_interface.find_one.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_find_user_invalid_successful(self, user_interface: Mock):
        user_interface.find_one.return_value = Mock(
            to_mongo=Mock(return_value={})
        )
        params = dict(invalid=True)
        response = self.client.get(self.route, params=params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_find_user_not_found(self, user_interface: Mock):
        user_interface.find_one.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


class UpdateUserRouteTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test4@test.com'
        self.valid_data = {
            'name': 'other',
            'gender': 'F',
        }

    @patch(solve_path('UserInterface'))
    def test_update_user_successful(self, user_interface: Mock):
        user_interface.find_one.return_value = Mock(
            to_mongo=Mock(return_value={})
        )

        response = self.client.put(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_update_user_not_found(self, user_interface: Mock):
        user_interface.find_one.return_value = None

        response = self.client.put(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)


class DeleteUserRouteTestCase(TestCase):
    def setUp(self):
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test4@test.com'

    @patch(solve_path('UserInterface'))
    def test_delete_user_successful(self, user_interface: Mock):
        user_interface.find_one.return_value = Mock()

        response = self.client.delete(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_delete_user_not_found(self, user_interface: Mock):
        user_interface.find_one.return_value = None

        response = self.client.delete(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

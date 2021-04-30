from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = 'src.routes.credentials'
    return ".".join([source, path])


class ValidateCredentialsRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(
            email='test1@test.com',
            password='any_password'
        )
        self.route = '/user/credentials'

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_validate_credentials_successful(
            self,
            user_interface: Mock,
            credential_interface: Mock
    ):
        user_interface.return_value = Mock()
        credential_interface.find_one.return_value = Mock(
            password='any_password'
        )

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_validate_credentials_not_found(self, user_interface: Mock):
        user_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_validate_credentials_invalid_credential(
            self,
            user_interface: Mock,
            credential_interface: Mock
    ):
        user_interface.return_value = Mock()
        credential_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_validate_credentials_invalid_password(
            self,
            user_interface: Mock,
            credential_interface: Mock
    ):
        user_interface.return_value = Mock()
        credential_interface.find_one.return_value = Mock(
            password='other'
        )

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class FindSecurityQuestionsRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test2@test.com/questions'

    @patch(solve_path('QuestionInterface'))
    @patch(solve_path('UserInterface'))
    def test_find_security_question_successful(
            self,
            user_interface: Mock,
            ques_interface: Mock
    ):
        user_interface.return_value = Mock()
        ques_interface.find_one.return_value = Mock(questions=[])

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_find_security_question_user_not_found(
            self,
            user_interface: Mock
    ):
        user_interface.find_one.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('QuestionInterface'))
    @patch(solve_path('UserInterface'))
    def test_find_security_question_questions_not_found(
            self,
            user_interface: Mock,
            ques_interface: Mock
    ):
        user_interface.return_value = Mock()
        ques_interface.find_one.return_value = None

        response = self.client.get(self.route)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class SetSecurityQuestionsRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = [dict(question='', answer='')]
        self.route = '/user/test3@test.com/questions'

    @patch(solve_path('QuestionInterface'))
    @patch(solve_path('UserInterface'))
    def test_set_security_question_successful(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.return_value = Mock()
        question_interface.find_one.return_value = Mock()

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_set_security_question_user_not_found(
            self,
            user_interface: Mock
    ):
        user_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('QuestionInterface'))
    @patch(solve_path('UserInterface'))
    def test_set_security_question_not_found(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.return_value = Mock()
        question_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class UpdatePasswordRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.valid_data = dict(email='test4@test.com', password='12345')
        self.route = '/user/password'

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_update_password_successful(
            self,
            user_interface: Mock,
            credential_interface: Mock,
    ):
        user_interface.find_one_active.return_value = Mock()
        credential_interface.find_one.return_value = Mock(password='12345')

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_update_password_user_not_found(
            self,
            user_interface: Mock
    ):
        user_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_update_password_credentials_not_found(
            self,
            user_interface: Mock,
            credential_interface: Mock,
    ):
        user_interface.find_one.return_value = Mock()
        credential_interface.find_one.return_value = None

        response = self.client.post(self.route, json=self.valid_data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class SetSecurityCodeRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test5@test.com/security_code'
        self.params = dict(email='test5@test.com', code='918273')

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_set_security_code_successful(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.find_one.return_value = Mock()
        question_interface.find_one.return_value = Mock(security_code='1234')

        response = self.client.post(self.route, params=self.params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_set_security_code_user_not_found(
            self,
            user_interface: Mock
    ):
        user_interface.find_one.return_value = None

        response = self.client.post(self.route, params=self.params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_set_security_code_credential_not_found(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.find_one.return_value = Mock()
        question_interface.find_one.return_value = None

        response = self.client.post(self.route, params=self.params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)


class GetSecurityCodeRouteTestCase(TestCase):

    def setUp(self) -> None:
        from src.api import app
        self.client = TestClient(app)

        self.route = '/user/test6@test.com/security_code'
        self.params = dict(email='test6@test.com')

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_get_security_code_successful(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.find_one.return_value = Mock()
        question_interface.find_one.return_value = Mock(security_code='1234')

        response = self.client.get(self.route, params=self.params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    @patch(solve_path('UserInterface'))
    def test_get_security_code_user_not_found(
            self,
            user_interface: Mock,
    ):
        user_interface.find_one.return_value = None

        response = self.client.get(
            self.route,
            params=self.params
        )

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 404)

    @patch(solve_path('CredentialInterface'))
    @patch(solve_path('UserInterface'))
    def test_get_security_code_credential_not_found(
            self,
            user_interface: Mock,
            question_interface: Mock,
    ):
        user_interface.find_one.return_value = Mock()
        question_interface.find_one.return_value = None

        response = self.client.get(self.route, params=self.params)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

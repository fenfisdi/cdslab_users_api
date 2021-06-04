from logging import setLoggerClass
from unittest import TestCase
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient


def solve_path(path: str):
    source = 'src.routes.root'
    return ".".join([source, path])


class CreateRootUserTestCase(TestCase):
    def setUp(self) -> None:
        from src.api import app
        self.client =TestClient(app)

        self.route = "/user"
        self.data = "email@test.com"

    @patch(solve_path("UserInterface"))
    def test_create_root_user(self, user_interface: Mock):
        user_interface.find.one.return_value = Mock()

        response = self.client.post(self.route, json=self.data)

        self.assertIsNotNone(response)

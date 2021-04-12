from unittest import TestCase

from fastapi.responses import Response

from src.utils.response import UJSONResponse


class ResponseTestCase(TestCase):

    def test_create_response(self):
        dict_result = {
            'message': 'any',
            'status_code': 200,
            'data': None,
        }
        result = UJSONResponse('any', 200)
        self.assertIsInstance(result, Response)

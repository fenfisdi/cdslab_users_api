from datetime import datetime
from unittest import TestCase

from mongoengine import connect, disconnect, Document

from src.models.db_models.base import BaseDocument


class BaseDocumentTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

    def tearDown(self):
        disconnect()

    def test_base_document_creation(self):
        mock_date = datetime(2021, 4, 12)

        result = BaseDocument(
            inserted_at=mock_date,
            updated_at=mock_date
        )

        self.assertIsInstance(result, Document)

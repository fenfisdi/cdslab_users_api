from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces import QuestionInterface
from src.models.db_models.user import Question, User, SecurityQuestions


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

        SecurityQuestions(
            user=self.user_1,
            questions=[Question(
                question="any_question",
                answer="any_answer"
            )]
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        result = QuestionInterface.find_one(self.user_1)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, SecurityQuestions)

    def test_find_one_not_found(self):
        result = QuestionInterface.find_one(self.user_2)

        self.assertIsNone(result)

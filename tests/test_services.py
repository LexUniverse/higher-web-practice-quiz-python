import pytest

from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService

pytestmark = pytest.mark.django_db


class TestCategoryService:
    def test_create_and_get_category(self):
        service = CategoryService()
        count_before = Category.objects.count()

        category = service.create_category('Science')

        assert Category.objects.count() == count_before + 1
        fetched = service.get_category(category.id)
        assert fetched.title == 'Science'

    def test_update_category(self, category):
        service = CategoryService()
        updated = service.update_category(category.id, {'title': 'New Title'})
        category.refresh_from_db()

        assert updated.title == 'New Title'
        assert category.title == 'New Title'

    def test_delete_category(self, category):
        service = CategoryService()
        category_id = category.id
        count_before = Category.objects.count()

        service.delete_category(category_id)

        assert Category.objects.count() == count_before - 1
        with pytest.raises(Category.DoesNotExist):
            service.get_category(category_id)


class TestQuizService:
    def test_get_quizes_by_title(self, quiz_factory):
        service = QuizService()
        quiz1 = quiz_factory('Математика для чайников')
        quiz2 = quiz_factory('Физика для чайников')

        results = service.get_quizes_by_title('чайников')
        assert len(results) == 2

        results = service.get_quizes_by_title('Математика')
        assert len(results) == 1
        assert results[0] == quiz1


class TestQuestionService:
    def test_check_answer(self, question):
        service = QuestionService()
        assert service.check_answer(question.id, '4') is True
        assert service.check_answer(question.id, '5') is False

    def test_random_question_from_quiz(self, quiz, question_factory, category):
        service = QuestionService()

        assert service.random_question_from_quiz(quiz.id) is None

        q1 = question_factory(quiz, category, text='q1')
        q2 = question_factory(quiz, category, text='q2')

        random_q = service.random_question_from_quiz(quiz.id)
        assert random_q is not None
        assert random_q in [q1, q2]

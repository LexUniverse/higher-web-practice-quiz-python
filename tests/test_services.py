import pytest
from django.http import Http404

from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService

pytestmark = pytest.mark.django_db


class TestCategoryService:
    def test_create_and_get_category(self):
        service = CategoryService()
        category_title = 'Science'
        count_before = Category.objects.count()

        category = service.create_category(category_title)
        assert Category.objects.count() == count_before + 1

        fetched = service.get_category(category.id)
        assert fetched.title == category_title

    def test_update_category(self, category):
        service = CategoryService()
        new_title = 'New Title'

        updated = service.update_category(category.id, {'title': new_title})
        category.refresh_from_db()

        assert updated.title == new_title
        assert category.title == new_title

    def test_delete_category(self, category):
        service = CategoryService()
        category_id = category.id
        count_before = Category.objects.count()

        service.delete_category(category_id)

        assert Category.objects.count() == count_before - 1
        with pytest.raises(Http404):
            service.get_category(category_id)


class TestQuizService:

    def test_get_quizes_by_title(self, quiz_factory):
        service = QuizService()
        title1 = 'Математика для чайников'
        title2 = 'Физика для чайников'
        search_common = 'чайников'
        search_specific = 'Математика'

        quiz1 = quiz_factory(title1)
        quiz_factory(title2)

        results = service.get_quizes_by_title(search_common)
        assert len(results) == 2

        results = service.get_quizes_by_title(search_specific)
        assert len(results) == 1
        assert results[0] == quiz1


class TestQuestionService:

    def test_check_answer(self, question):
        service = QuestionService()
        correct_answer = '4'
        wrong_answer = '5'

        assert service.check_answer(question.id, correct_answer) is True
        assert service.check_answer(question.id, wrong_answer) is False

    def test_random_question_from_quiz(self, quiz, question_factory, category):
        service = QuestionService()
        assert service.random_question_from_quiz(quiz.id) is None

        q1 = question_factory(quiz, category, text='q1')
        q2 = question_factory(quiz, category, text='q2')

        random_q = service.random_question_from_quiz(quiz.id)

        assert random_q is not None
        assert random_q in [q1, q2]

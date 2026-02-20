import pytest
from rest_framework.test import APIClient

from quiz.models import Category, Difficulty, Question, Quiz


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API."""
    return APIClient()


@pytest.fixture
def category_factory(db):
    """Фабрика для создания категорий."""
    def create_category(title: str):
        return Category.objects.create(title=title)
    return create_category


@pytest.fixture
def category(category_factory):
    """Фикстура для одной категории."""
    return category_factory('Математика')


@pytest.fixture
def another_category(category_factory):
    """Фикстура для второй категории."""
    return category_factory('История')


@pytest.fixture
def quiz_factory(db):
    """Фабрика для создания квизов."""
    def create_quiz(title: str, description: str = ''):
        return Quiz.objects.create(title=title, description=description)
    return create_quiz


@pytest.fixture
def quiz(quiz_factory):
    """Фикстура для одного квиза."""
    return quiz_factory('Базовая арифметика', 'Проверь свои знания.')


@pytest.fixture
def question_factory(db):
    """Фабрика для создания вопросов."""
    def create_question(quiz: Quiz, category: Category, text: str, **kwargs):
        defaults = {
            'options': ['3', '4', '5'],
            'correct_answer': '4',
            'difficulty': Difficulty.EASY
        }
        defaults.update(kwargs)
        return Question.objects.create(quiz=quiz, category=category, text=text, **defaults)
    return create_question


@pytest.fixture
def question(question_factory, quiz, category):
    """Фикстура для одного вопроса."""
    return question_factory(quiz, category, text='Сколько будет 2+2?')

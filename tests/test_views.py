import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestCategoryAPI:
    def test_get_category_list_empty(self, api_client):
        """GET /api/category/: Ответ - пустой список, если категорий нет."""
        url = reverse('quiz:category-create')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_category_list_with_content(self, api_client, category, another_category):
        """GET /api/category/: Успешное получение списка категорий."""
        url = reverse('quiz:category-create')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

        assert {'id': another_category.id,
                'title': another_category.title} in data
        assert {'id': category.id, 'title': category.title} in data

    def test_create_category_success(self, api_client):
        """POST /api/category/: Успешное создание категории."""
        url = reverse('quiz:category-create')
        new_title = 'География'

        response = api_client.post(url, {'title': new_title}, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert 'id' in data
        assert data['title'] == new_title

    def test_create_category_bad_request(self, api_client):
        """POST /api/category/: Ошибка 400, если не передать title."""
        url = reverse('quiz:category-create')
        response = api_client.post(url, {}, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_category(self, api_client, category):
        """DELETE /api/category/<id>/: Успешное удаление."""
        url = reverse('quiz:category-detail',
                      kwargs={'category_id': category.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestQuizAPI:

    def test_get_single_quiz_detail(self, api_client, quiz, question):
        """GET /api/quiz/<id>/: Успешное получение квиза с вопросами."""
        url = reverse('quiz:quiz-detail', kwargs={'quiz_id': quiz.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['id'] == quiz.id
        assert data['title'] == quiz.title
        assert 'questions' in data
        assert len(data['questions']) == 1

        question_data = data['questions'][0]
        assert question_data['id'] == question.id
        assert question_data['text'] == question.text
        assert 'options' in question_data

    def test_get_quiz_by_title(self, api_client, quiz):
        """GET /api/quiz/by_title/<title>/: Поиск квиза по названию."""
        search_term = 'арифметика'
        url = reverse('quiz:quiz-by-title', kwargs={'title': search_term})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]['title'] == quiz.title


class TestQuestionAPI:

    def test_create_question_validation_error(self, api_client, quiz, category):
        """POST /api/question/: Ошибка валидации (мало вариантов)."""
        url = reverse('quiz:question-create')
        question_text = "Сколько будет один плюс ноль?"
        invalid_options = ["один"]
        correct_answer = "один"
        difficulty = "easy"

        payload = {
            "quiz": quiz.id,
            "category": category.id,
            "text": question_text,
            "options": invalid_options,
            "correct_answer": correct_answer,
            "difficulty": difficulty
        }

        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'options' in response.json()

    def test_check_answer_correct(self, api_client, question):
        """POST /api/question/<id>/check/: Проверка правильного ответа."""
        url = reverse('quiz:question-check-answer',
                      kwargs={'question_id': question.id})
        correct_answer = '4'

        response = api_client.post(
            url, {'answer': correct_answer}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'correct': True}

    def test_check_answer_incorrect(self, api_client, question):
        """POST /api/question/<id>/check/: Проверка неправильного ответа."""
        url = reverse('quiz:question-check-answer',
                      kwargs={'question_id': question.id})
        incorrect_answer = '5'
        response = api_client.post(
            url, {'answer': incorrect_answer}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'correct': False}

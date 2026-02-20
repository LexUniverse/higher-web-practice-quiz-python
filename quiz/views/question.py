"""Модуль с контроллерами для вопросов."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Question
from quiz.serializers import AnswerCheckSerializer, QuestionSerializer
from quiz.services.question import QuestionService

question_service = QuestionService()


class QuestionListCreateView(APIView):
    """
    GET /api/question/
    POST /api/question/
    """

    def get(self, request):
        """Получение списка всех вопросов."""

        questions = question_service.list_questions()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание нового вопроса."""

        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_question = question_service.create_question(
            data=serializer.validated_data)
        return Response(
            QuestionSerializer(created_question).data,
            status=status.HTTP_201_CREATED
        )


class QuestionDetailView(APIView):
    """
    GET /api/question/<id:int>/
    PUT /api/question/<id:int>/
    DELETE /api/question/<id:int>/
    """

    def get(self, request, question_id: int):
        """Получение вопроса по ID."""

        try:
            question = question_service.get_question(question_id)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, question_id: int):
        """Обновление вопроса."""

        try:
            serializer = QuestionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_question = question_service.update_question(
                question_id=question_id,
                data=serializer.validated_data
            )
            return Response(QuestionSerializer(updated_question).data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, question_id: int):
        """Удаление вопроса."""

        try:
            question_service.delete_question(question_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class QuestionByTextView(APIView):
    """GET /api/question/by_text/<query: str>/"""

    def get(self, request, query: str):
        """Получение вопросов по тексту."""
        questions = question_service.get_questions_by_text(query)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class CheckAnswerView(APIView):
    """POST /api/question/<id:int>/check/"""

    def post(self, request, question_id: int):
        """Проверка ответа на вопрос."""

        try:
            serializer = AnswerCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_answer = serializer.validated_data.get('answer')
            is_correct = question_service.check_answer(
                question_id, user_answer)
            return Response({"correct": is_correct})
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

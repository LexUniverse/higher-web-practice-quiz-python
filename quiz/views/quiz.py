"""Модуль с контроллерами для квизов."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.serializers import (QuestionSerializer, QuizDetailSerializer,
                              QuizSerializer)
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService

quiz_service = QuizService()
question_service = QuestionService()


class QuizListCreateView(APIView):
    """Контроллер для получения списка или создания одного квиза.

    GET /api/quiz/
    POST /api/quiz/
    """

    def get(self, request):
        """Получение списка всех квизов."""
        quizzes = quiz_service.list_quizzes()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Создание нового квиза."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_quiz = quiz_service.create_quiz(data=serializer.validated_data)
        return Response(
            QuizSerializer(created_quiz).data,
            status=status.HTTP_201_CREATED
        )


class QuizDetailView(APIView):
    """Контроллер для работы с одним квизом.

    GET /api/quiz/<id:int>/
    PUT /api/quiz/<id:int>/
    DELETE /api/quiz/<id:int>/
    """

    def get(self, request, quiz_id: int):
        """Получение квиза по ID с вопросами."""
        quiz = quiz_service.get_quiz(quiz_id)
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, quiz_id: int):
        """Обновление квиза."""
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_quiz = quiz_service.update_quiz(
            quiz_id=quiz_id,
            data=serializer.validated_data
        )
        return Response(QuizSerializer(updated_quiz).data)

    def delete(self, request, quiz_id: int):
        """Удаление квиза."""
        quiz_service.delete_quiz(quiz_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizByTitleView(APIView):
    """GET /api/quiz/by_title/<title: str>/"""

    def get(self, request, title: str):
        """Получение квиза по названию."""
        quizzes = quiz_service.get_quizes_by_title(title)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class RandomQuestionView(APIView):
    """GET /api/quiz/<id:int>/random_question/"""

    def get(self, request, quiz_id: int):
        """Получение случайного вопроса из квиза."""
        quiz_service.get_quiz(quiz_id)
        question = question_service.random_question_from_quiz(quiz_id)
        if not question:
            return Response(
                {"detail": "В этом квизе нет вопросов."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

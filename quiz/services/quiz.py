"""Модуль с реализацией сервиса квизов."""

from quiz.dao import AbstractQuizService
from quiz.models import Quiz


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза."""

    def list_quizzes(self) -> list[Quiz]:
        return list(Quiz.objects.all())

    def get_quiz(self, quiz_id: int) -> Quiz:
        return Quiz.objects.get(id=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        return list(Quiz.objects.filter(title__icontains=title))

    def create_quiz(self, data: dict) -> Quiz:
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        quiz = self.get_quiz(quiz_id)
        for key, value in data.items():
            setattr(quiz, key, value)
        quiz.save()
        return quiz

    def delete_quiz(self, quiz_id: int) -> None:
        quiz = self.get_quiz(quiz_id)
        quiz.delete()

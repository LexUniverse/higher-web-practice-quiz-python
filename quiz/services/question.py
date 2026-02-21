"""Модуль с реализацией сервиса вопросов."""

import random

from django.shortcuts import get_object_or_404

from quiz.dao import AbstractQuestionService
from quiz.models import Question
from quiz.services.utils import update_object


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов."""

    def list_questions(self) -> list[Question]:
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        return get_object_or_404(Question, id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, data: dict) -> Question:
        return Question.objects.create(**data)

    def update_question(self, question_id: int, data: dict) -> Question:
        return update_object(Question, question_id, data)

    def delete_question(self, question_id: int) -> None:
        self.get_question(question_id).delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        question = self.get_question(question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question | None:
        questions = self.get_questions_for_quiz(quiz_id)
        if not questions:
            return None
        return random.choice(questions)

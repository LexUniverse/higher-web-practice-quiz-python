"""Модуль с реализацией сервиса вопросов."""

from quiz.dao import AbstractQuestionService
from quiz.models import Question


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов."""

    def list_questions(self) -> list[Question]:
        return list(Question.objects.all())

    def get_question(self, question_id: int) -> Question:
        return Question.objects.get(id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        return list(Question.objects.filter(text__icontains=text))

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        return list(Question.objects.filter(quiz_id=quiz_id))

    def create_question(self, data: dict) -> Question:
        return Question.objects.create(**data)

    def update_question(self, question_id: int, data: dict) -> Question:
        question = self.get_question(question_id)
        for key, value in data.items():
            setattr(question, key, value)
        question.save()
        return question

    def delete_question(self, question_id: int) -> None:
        question = self.get_question(question_id)
        question.delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        question = self.get_question(question_id)
        return question.correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        question = Question.objects.filter(
            quiz_id=quiz_id).order_by('?').first()
        return question

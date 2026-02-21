"""Модуль c моделями приложения quiz."""

from django.db import models

from quiz import constants
from quiz.validators import validate_min_options


class Category(models.Model):
    """Модель категории вопросов."""

    title = models.CharField(
        max_length=constants.CATEGORY_TITLE_MAX_LENGTH,
        verbose_name='Название категории',
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title[:constants.PREVIEW_TEXT_LENGTH]


class Quiz(models.Model):
    """Модель квиза."""

    title = models.CharField(
        max_length=constants.QUIZ_TITLE_MAX_LENGTH,
        verbose_name='Название квиза'
    )
    description = models.CharField(
        max_length=constants.QUIZ_DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Описание квиза'
    )

    class Meta:
        verbose_name = 'Квиз'
        verbose_name_plural = 'Квизы'
        ordering = ['title']

    def __str__(self):
        return self.title[:constants.PREVIEW_TEXT_LENGTH]


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов."""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса."""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='Квиз',
        related_name='questions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='questions'
    )
    text = models.CharField(
        max_length=constants.QUESTION_TEXT_MAX_LENGTH,
        verbose_name='Текст вопроса'
    )
    description = models.CharField(
        max_length=constants.QUESTION_DESCRIPTION_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Описание вопроса'
    )
    options = models.JSONField(
        verbose_name='Варианты ответа (массив)',
        validators=[validate_min_options]
    )
    correct_answer = models.CharField(
        max_length=constants.CORRECT_ANSWER_MAX_LENGTH,
        verbose_name='Правильный ответ'
    )
    explanation = models.CharField(
        max_length=constants.EXPLANATION_MAX_LENGTH,
        blank=True,
        null=True,
        verbose_name='Объяснение ответа'
    )
    difficulty = models.CharField(
        max_length=constants.DIFFICULTY_MAX_LENGTH,
        choices=Difficulty.choices,
        verbose_name='Сложность'
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-id']

    def __str__(self):
        return self.text[:constants.PREVIEW_TEXT_LENGTH]

"""Модуль c сериализаторами."""

from rest_framework import serializers

from quiz.models import Category, Question, Quiz
from quiz.validators import validate_min_options


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('id', 'title')


class AnswerCheckSerializer(serializers.Serializer):
    answer = serializers.CharField()


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов."""

    quiz = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Question
        fields = (
            'id',
            'quiz',
            'category',
            'text',
            'description',
            'options',
            'correct_answer',
            'explanation',
            'difficulty'
        )

    def validate_options(self, value):
        validate_min_options(value)
        return value

    def validate(self, data):
        correct_answer = data.get('correct_answer')
        options = data.get('options')

        if correct_answer and options:
            if correct_answer not in options:
                raise serializers.ValidationError({
                    "correct_answer": "Правильный ответ должен быть одним "
                    "из вариантов в `options`."
                })
        return data


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description')


class QuizDetailSerializer(QuizSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ('questions',)

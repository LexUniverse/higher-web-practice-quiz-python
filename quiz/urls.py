"""Модуль c роутингом для приложения quiz."""

from django.urls import path

from quiz.views import category, question, quiz

app_name = 'quiz'

urlpatterns = [
    path(
        'category/',
        category.CategoryListCreateView.as_view(),
        name='category-create'
    ),
    path(
        'category/<int:category_id>/',
        category.CategoryDetailView.as_view(),
        name='category-detail'
    ),

    path(
        'quiz/',
        quiz.QuizListCreateView.as_view(),
        name='quiz-create'
    ),
    path(
        'quiz/<int:quiz_id>/',
        quiz.QuizDetailView.as_view(),
        name='quiz-detail'
    ),
    path(
        'quiz/by_title/<str:title>/',
        quiz.QuizByTitleView.as_view(),
        name='quiz-by-title'
    ),
    path(
        'quiz/<int:quiz_id>/random_question/',
        quiz.RandomQuestionView.as_view(),
        name='quiz-random-question'
    ),

    path(
        'question/',
        question.QuestionListCreateView.as_view(),
        name='question-create'
    ),
    path(
        'question/<int:question_id>/',
        question.QuestionDetailView.as_view(),
        name='question-detail'
    ),
    path(
        'question/by_text/<str:query>/',
        question.QuestionByTextView.as_view(),
        name='question-by-text'
    ),
    path(
        'question/<int:question_id>/check/',
        question.CheckAnswerView.as_view(),
        name='question-check-answer'
    ),
]

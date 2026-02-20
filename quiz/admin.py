from django.contrib import admin

from .models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'question_count'
    )
    search_fields = ('title',)

    def question_count(self, obj):
        return obj.questions.count()

    question_count.short_description = 'Кол-во вопросов'


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = (
        'text',
        'category',
        'difficulty',
        'options',
        'correct_answer'
    )
    ordering = ('id',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'question_count')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()

    question_count.short_description = 'Кол-во вопросов'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'quiz', 'category', 'difficulty')

    list_editable = ('difficulty',)

    list_filter = ('difficulty', 'quiz', 'category')

    search_fields = ('text', 'explanation')

    fieldsets = (
        ('Основная информация', {
            'fields': ('quiz', 'category', 'text', 'description')
        }),
        ('Ответы', {
            'fields': ('options', 'correct_answer', 'explanation'),
            'description': "Укажите варианты ответа в формате JSON-массива"
            " и выберите правильный."
        }),
        ('Метаданные', {
            'fields': ('difficulty',)
        }),
    )

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст вопроса'

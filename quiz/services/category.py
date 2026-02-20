"""Модуль с реализацией сервиса категорий."""

from quiz.dao import AbstractCategoryService
from quiz.models import Category


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий."""

    def list_categories(self) -> list[Category]:
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category:
        return Category.objects.get(id=category_id)

    def create_category(self, title: str) -> Category:
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category:
        category = self.get_category(category_id)
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete_category(self, category_id: int) -> None:
        category = self.get_category(category_id)
        category.delete()

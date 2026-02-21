from django.shortcuts import get_object_or_404

from quiz.dao import AbstractCategoryService
from quiz.models import Category
from quiz.services.utils import update_object


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий."""

    def list_categories(self) -> list[Category]:
        return list(Category.objects.all())

    def get_category(self, category_id: int) -> Category:
        return get_object_or_404(Category, id=category_id)

    def create_category(self, title: str) -> Category:
        category, _ = Category.objects.get_or_create(title=title)
        return category

    def update_category(self, category_id: int, data: dict) -> Category:
        return update_object(Category, category_id, data)

    def delete_category(self, category_id: int) -> None:
        self.get_category(category_id).delete()

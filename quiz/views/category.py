"""Модуль с контроллерами для категорий."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Category
from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService

category_service = CategoryService()


class CategoryListCreateView(APIView):
    """Контроллер для получения списка категорий и создания новой категории.

    GET /api/category/
    POST /api/category/
    """

    def get(self, request):
        """Получение списка всех категорий."""
        categories = category_service.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Создание новой категории."""
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_category = category_service.create_category(
            title=serializer.validated_data.get('title')
        )
        return Response(
            CategorySerializer(created_category).data,
            status=status.HTTP_201_CREATED
        )


class CategoryDetailView(APIView):
    """Контроллер для работы с одной категорией (получение, обновление, удаление).

    GET /api/category/<id:int>/
    PUT /api/category/<id:int>/
    DELETE /api/category/<id:int>/
    """

    def get(self, request, category_id: int):
        """Получение категории по ID."""
        try:
            category = category_service.get_category(category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, category_id: int):
        """Обновление категории."""
        try:
            serializer = CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_category = category_service.update_category(
                category_id=category_id,
                data=serializer.validated_data
            )
            return Response(CategorySerializer(updated_category).data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, category_id: int):
        """Удаление категории."""
        try:
            category_service.delete_category(category_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

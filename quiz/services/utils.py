from django.db import models
from django.shortcuts import get_object_or_404


def update_object(model: type[models.Model], pk: int, data: dict):
    """
    Утилита для обновления полей объекта модели.

    Получает объект по pk, итерируется по словарю data
    и устанавливает соответствующие атрибуты.
    """
    obj = get_object_or_404(model, pk=pk)
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return obj

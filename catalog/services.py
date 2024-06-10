from django.core.cache import cache

from config.settings import CACHE_ENABLED
from catalog.models import Category


def get_categories_from_cache():
    """
    Получает список категорий из кэша. Если кэш пуст, получает данные из БД
    """
    if not CACHE_ENABLED:
        return Category.objects.all()
    else:
        key = 'category_list'
        categories = cache.get(key)
        if categories is not None:
            return categories
        categories = Category.objects.all()
        cache.set(key, categories)
        return categories

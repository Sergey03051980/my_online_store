from django.core.cache import cache
from .models import Product, Category


class ProductService:
    """Сервис для кеширования операций с продуктами"""

    @staticmethod
    def get_cached_products():
        cache_key = 'published_products'
        products = cache.get(cache_key)

        if products is None:
            products = Product.objects.filter(is_published=True).select_related('owner')
            cache.set(cache_key, products, 60 * 5)
        return products

    @staticmethod
    def get_cached_product(pk):
        cache_key = f'product_{pk}'
        product = cache.get(cache_key)

        if product is None:
            try:
                product = Product.objects.select_related('owner').get(pk=pk)
                cache.set(cache_key, product, 60 * 15)
            except Product.DoesNotExist:
                product = None
        return product

    @staticmethod
    def clear_product_cache(pk=None):
        if pk:
            cache.delete(f'product_{pk}')
        cache.delete('published_products')

    @staticmethod
    def get_products_by_category(category_slug):
        """Для будущего использования - продукты по категории"""
        cache_key = f'products_category_{category_slug}'
        products = cache.get(cache_key)

        if products is None:
            try:
                category = Category.objects.get(slug=category_slug)
                products = Product.objects.filter(
                    category=category,
                    is_published=True
                ).select_related('owner', 'category')
                cache.set(cache_key, products, 60 * 10)
            except Category.DoesNotExist:
                products = Product.objects.none()
        return products

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from .models import Product
from .forms import ProductForm


# Сервис для работы с кешированием продуктов
class ProductService:
    @staticmethod
    def get_cached_products():
        """Кешированный список всех опубликованных продуктов"""
        cache_key = 'published_products'
        products = cache.get(cache_key)

        if products is None:
            products = Product.objects.filter(is_published=True).select_related('owner')
            cache.set(cache_key, products, 60 * 5)  # 5 минут
        return products

    @staticmethod
    def get_cached_product(pk):
        """Кешированный продукт по ID"""
        cache_key = f'product_{pk}'
        product = cache.get(cache_key)

        if product is None:
            try:
                product = Product.objects.select_related('owner').get(pk=pk)
                cache.set(cache_key, product, 60 * 15)  # 15 минут
            except Product.DoesNotExist:
                product = None
        return product

    @staticmethod
    def clear_product_cache(pk=None):
        """Очистка кеша продуктов"""
        if pk:
            cache.delete(f'product_{pk}')
        cache.delete('published_products')


# Кеширование на 5 минут для списка продуктов
@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Используем кешированный сервис вместо прямого запроса
        return ProductService.get_cached_products()


# Кеширование на 15 минут для детальной страницы
@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Используем кешированный сервис
        return ProductService.get_cached_product(self.kwargs.get('pk'))


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # Очищаем кеш после создания нового продукта
        ProductService.clear_product_cache()
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        # Очищаем кеш этого продукта после обновления
        ProductService.clear_product_cache(self.object.pk)
        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        return (product.owner == self.request.user or
                self.request.user.has_perm('catalog.delete_product'))

    def delete(self, request, *args, **kwargs):
        # Сохраняем ID перед удалением для очистки кеша
        product_id = self.get_object().pk
        response = super().delete(request, *args, **kwargs)
        # Очищаем кеш после удаления
        ProductService.clear_product_cache(product_id)
        return response


class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.is_published = False
        product.save()
        # Очищаем кеш после снятия с публикации
        ProductService.clear_product_cache(pk)
        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect('catalog:product_detail', pk=product.pk)


# Кеширование контактов на 1 час
@method_decorator(cache_page(60 * 60), name='dispatch')
class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

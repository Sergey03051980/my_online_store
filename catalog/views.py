from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.conf import settings
from .models import Product
from .forms import ProductForm


def home(request):
    products_list = Product.objects.all()

    paginator = Paginator(products_list, settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {
        'page_obj': page_obj,
    })


def contacts(request):
    return render(request, 'catalog/contacts.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_add(request):
    """Функция для добавления товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')  # ← ВАЖНО: используйте правильное имя
    else:
        form = ProductForm()

    return render(request, 'catalog/product_form.html', {'form': form})


def product_delete(request, pk):
    """Функция для удаления товара"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('catalog:home')  # ← Тоже исправьте здесь, если нужно

    return render(request, 'catalog/product_confirm_delete.html', {'product': product})

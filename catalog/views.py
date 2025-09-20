from django.shortcuts import render
from .models import Product  # Это правильный импорт!

def home(request):
    latest_products = Product.objects.all().order_by('-created_at')[:5]
    print("Последние 5 продуктов:", [p.name for p in latest_products])
    return render(request, 'catalog/home.html')

def contacts(request):
    return render(request, 'catalog/contacts.html')

from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')  # что показывать в списке
    list_display_links = ('id', 'name')  # что будет ссылкой на редактирование
    search_fields = ('name', 'description')  # по каким полям можно искать
    list_filter = ('name',)  # фильтрация по полям


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')  # поля в списке
    list_display_links = ('id', 'name')  # ссылки для редактирования
    list_filter = ('category', 'created_at')  # фильтры справа
    search_fields = ('name', 'description')  # поиск по названию и описанию
    list_editable = ('price',)  # поля которые можно редактировать прямо в списке

    # Дополнительные настройки (опционально)
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'price')
        }),
        ('Описание', {
            'fields': ('description', 'image'),
            'classes': ('collapse',)  # свернуть раздел по умолчанию
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at')  # поля только для чтения

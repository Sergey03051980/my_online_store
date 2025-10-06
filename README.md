# My Online Store 🛍️

Веб-приложение интернет-магазина на Django с полным функционалом CRUD для управления продуктами.

## 🚀 Функциональность

### 📦 Управление продуктами (CRUD)
- **Создание** продуктов через формы Django
- **Просмотр** детальной информации о продуктах
- **Редактирование** существующих продуктов
- **Удаление** продуктов с подтверждением

### 🛡️ Валидация форм
- **Запрещенные слова** в названии и описании (казино, криптовалюта, биржа и др.)
- **Проверка цены** - нельзя установить отрицательную цену
- **Стилизация полей** через кастомный метод `__init__`

### 🎨 Интерфейс
- Адаптивный дизайн с Bootstrap
- Хлебные крошки для навигации
- Карточки товаров с изображениями
- Красивые формы с валидацией

## 🛠️ Технологии

- **Backend**: Django 5.2.6
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite
- **Template Engine**: Django Templates
- **Forms**: Django ModelForms

## 📁 Структура проекта
my_online_store/
├── catalog/ # Основное приложение
│ ├── models.py # Модели Product, Category, BlogPost
│ ├── forms.py # Формы с валидацией
│ ├── views.py # CBV для CRUD операций
│ ├── urls.py # Маршрутизация
│ └── templates/ # Шаблоны
│ ├── base.html # Базовый шаблон
│ ├── home.html # Главная страница
│ ├── product_form.html # Форма создания/редактирования
│ ├── product_detail.html # Детали продукта
│ └── product_confirm_delete.html # Подтверждение удаления
├── config/ # Настройки проекта
└── manage.py # Django management script

text

## 🚀 Установка и запуск

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd my_online_store
Установка зависимостей

bash
poetry install
Настройка базы данных

bash
python manage.py makemigrations
python manage.py migrate
Создание суперпользователя

bash
python manage.py createsuperuser
Запуск сервера

bash
python manage.py runserver
Открыть в браузере

text
http://127.0.0.1:8000/
📋 Основные URL
URL	Назначение
/	Главная страница со списком товаров
/product/create/	Создание нового продукта
/product/<id>/	Просмотр деталей продукта
/product/<id>/update/	Редактирование продукта
/product/<id>/delete/	Удаление продукта
/contacts/	Страница контактов
/admin/	Админ-панель Django
🎯 Особенности реализации
Валидация форм
python
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 
                   'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):
    def clean_name(self):
        # Проверка на запрещенные слова в названии
        pass
    
    def clean_description(self):
        # Проверка на запрещенные слова в описании
        pass
    
    def clean_price(self):
        # Проверка что цена не отрицательная
        pass
Стилизация форм
python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field_name, field in self.fields.items():
        field.widget.attrs['class'] = 'form-control'
👨‍💻 Разработчик
Студент: [Сергей Иващенко]

Курс: Django

Задание: 26.1 - Формы и валидация
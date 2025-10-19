from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создание групп и назначение прав'

    def handle(self, *args, **options):
        # Создаем группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем разрешения для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Добавляем права модератору
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=[
                'can_unpublish_product',  # Кастомное право
                'delete_product',  # Удаление любого продукта
                'change_product',  # Изменение любого продукта
                'view_product',  # Просмотр любого продукта
            ]
        )

        moderator_group.permissions.set(permissions)

        self.stdout.write(
            self.style.SUCCESS('Права для группы "Модератор продуктов" назначены')
        )

        # Выводим список назначенных прав
        for perm in moderator_group.permissions.all():
            self.stdout.write(f' - {perm.name}')

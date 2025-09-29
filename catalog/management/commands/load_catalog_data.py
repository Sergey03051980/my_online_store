from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load catalog data from fixtures'

    def handle(self, *args, **options):
        self.stdout.write('Loading catalog data from fixtures...')

        # Загружаем фикстуры
        call_command('loaddata', 'categories.json')
        call_command('loaddata', 'products.json')

        self.stdout.write(
            self.style.SUCCESS('Catalog data successfully loaded!')
        )

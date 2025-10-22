from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    def handle(self, *args, **options):
        cache.set('test_key', 'Hello Redis!', 30)
        value = cache.get('test_key')
        if value:
            self.stdout.write(self.style.SUCCESS(f'Redis работает: {value}'))
        else:
            self.stdout.write(self.style.ERROR('Redis не работает'))

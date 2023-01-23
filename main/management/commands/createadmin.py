from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle(self, **options):
        from django.contrib.auth.models import User
        User.objects.create_superuser('admin', '7upnamk@gmail.com', 'admin')

from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        from main import signals  
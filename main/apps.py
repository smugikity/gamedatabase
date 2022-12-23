from django.apps import AppConfig

class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        from main import signals  

from django.apps import AppConfig


class BookaboothDjangoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BookABooth_Django'

    def ready(self):
        from . import scheduler
        scheduler.start()

from django.apps import AppConfig


class GifterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gifter'

    def ready(self):
        # Required to register signals
        import gifter.signals as _

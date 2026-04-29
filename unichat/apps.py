from django.apps import AppConfig


class UnichatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'unichat'

    def ready(self):
        import unichat.signals
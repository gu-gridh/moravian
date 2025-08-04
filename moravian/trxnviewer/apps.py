from django.apps import AppConfig


class TrxnviewerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trxnviewer'

    def ready(self):
        import trxnviewer.signals  # noqa: F401

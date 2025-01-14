from django.apps import AppConfig


class CertificationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'certification_app'

    def ready(self):
        import certification_app.signals

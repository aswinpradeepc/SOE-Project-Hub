from django.apps import AppConfig


class AuthLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_login'

    def ready(self):
        import auth_login.signals

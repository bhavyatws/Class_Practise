from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    #ready function connect signal with this app
    def ready(self):
          import home.signals

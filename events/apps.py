from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    verbose_name = 'Eventi'
    
    def ready(self):
        """
        Metodo chiamato quando l'app è pronta.
        Può essere usato per importare signal handlers.
        """
        pass
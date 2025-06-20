from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'
    verbose_name = 'Prenotazioni'
    
    def ready(self):
        """
        Metodo chiamato quando l'app è pronta.
        Può essere usato per importare signal handlers.
        """
        # Importa i signals se necessario
        # from . import signals
        pass
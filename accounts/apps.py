from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Account Utenti'
    
    def ready(self):
        """
        Metodo chiamato quando l'app è pronta.
        Può essere usato per importare signal handlers.
        """
        # Importa i signals se necessario
        # from . import signals
        pass
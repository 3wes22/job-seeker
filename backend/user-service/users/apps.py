from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals  # Import signals
        # Kafka consumers should run in a dedicated process (e.g., management command)
        # to avoid duplicate consumers and lifecycle issues.
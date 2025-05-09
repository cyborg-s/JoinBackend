from django.apps import AppConfig

class JoinBeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'join_BE'

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.utils import OperationalError
        import logging

        logger = logging.getLogger(__name__)

        try:
            if not User.objects.filter(username='guest').exists():
                User.objects.create_user(
                    username='guest@example.com',
                    email='guest@example.com',
                    password='guestpassword123',
                    first_name='Guest'
                )
                logger.info("✅ Gastnutzer wurde automatisch erstellt.")
        except OperationalError:
            # DB ist evtl. noch nicht bereit (z. B. beim Migrationslauf)
            logger.warning("⚠️ Gastnutzer konnte nicht erstellt werden – DB noch nicht bereit.")
        except Exception as e:
            logger.error(f"❌ Fehler beim Erstellen des Gastnutzers: Gastzugang Exestiert bereits")



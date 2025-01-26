from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AdminSideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_side'

    def ready(self):
        from .models import ensure_default_tags
        post_migrate.connect(ensure_default_tags, sender=self)
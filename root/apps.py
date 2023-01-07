from django.apps import AppConfig
from django.db.models.signals import post_migrate
from Mainproject.db_default_migrations import create_migration

class RootConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'root'

    def ready(self):
        post_migrate.connect(create_migration, sender=self)
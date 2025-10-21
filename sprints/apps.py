from django.apps import AppConfig


class SprintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sprints'


    def ready(self):
        import sprints.signals # Import signals to ensure they are registered
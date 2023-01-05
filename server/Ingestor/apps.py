from django.apps import AppConfig



class IngestorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Ingestor"

    def ready(self):
        
        from Ingestor.signals import handleYoutubeVideoDelete
        
from Ingestor.models import YoutubeVideo
from django.db.models.signals import post_delete

def handleYoutubeVideoDelete(sender, instance, *args, **kwargs):
    from Index.index import Index
    Index().removeObjectFromIndex(instance)

post_delete.connect(handleYoutubeVideoDelete, YoutubeVideo, False, 'YoutubeVideoDelete')

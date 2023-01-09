from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import requests
import datetime
from Ingestor.models import Keys, RequestDetails
from Ingestor.util import utcDatetimeToRFC3339, utcRFC3339toDatetime, saveYoutubeVideoFromJson
import json
from Ingestor.models import YoutubeVideo

class Command(BaseCommand):

    help = 'yo sup'

    def add_arguments(self, parser) -> None:

        pass

    def handle(self, *args, **options):
        for video in YoutubeVideo.objects.all():
            video.save()
        

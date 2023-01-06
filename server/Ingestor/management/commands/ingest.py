from time import sleep
from django.core.management.base import BaseCommand, CommandError
import requests
import datetime
from Ingestor.models import Keys, RequestDetails
from Ingestor.util import utcDatetimeToRFC3339, utcRFC3339toDatetime, saveYoutubeVideoFromJson


def getDataFromYoutubeApi():
    url = 'https://youtube.googleapis.com/youtube/v3/search'

    api_keys = list(Keys.objects.filter(exhausted_on__date__lt=datetime.datetime.now(
    ).date()).order_by('-id').values_list('api_key', flat=True))
    active_api_key = api_keys[0]

    details = RequestDetails.objects.last()
    if not details:
        details = RequestDetails.objects.create(
            query='hindi | smartphone | it | fashion | female | male',
            published_after=datetime.datetime.now(datetime.timezone.utc)
        )

    response = requests.get(url=url, params={
        'part': 'snippet',
        'maxResults': 50,
        'order': 'date',
        'publishedAfter': utcDatetimeToRFC3339(details.published_after),
        'q': details.query,
        'type': 'video',
        'key': active_api_key,
        'pageToken': details.page_token
    })

    response = response.json()

    if 'items' in response:
        for item in response['items']:
            published_at = utcRFC3339toDatetime(
                item['snippet']['publishedAt'])

            # Reject entries which are older than the minimum time
            if published_at < details.published_after:
                break

            saveYoutubeVideoFromJson(item)
            
    # If there is still another page, we call the api again
    # until there are no more pages left
    if 'nextPageToken' in response:
        details.page_token = response['nextPageToken']
        details.save()
        getDataFromYoutubeApi()
    else:
        details.page_token = ''
        details.published_after = datetime.datetime.now(datetime.timezone.utc)
        details.save()
        return


class Command(BaseCommand):

    help = 'yo sup'

    def add_arguments(self, parser) -> None:

        pass

    def handle(self, *args, **options):

        counter = 1
        while (True):
            print(f'Getting Data from Api, iteration number {counter}')
            getDataFromYoutubeApi()
            counter += 1
            sleep(10)

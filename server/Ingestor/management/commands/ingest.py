from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
import requests
import datetime
from Ingestor.models import Keys, RequestDetails
from Ingestor.util import utcDatetimeToRFC3339, utcRFC3339toDatetime, saveYoutubeVideoFromJson
import json

def getApiKey() -> Keys:
    api_keys = list(Keys.objects.filter(Q(exhausted_on__date__lt=datetime.datetime.now(
    ).date())|Q(exhausted_on__isnull=True)).order_by('-id'))
    if not api_keys:
        print('No API Keys Left')
        return
    return api_keys[0]

def getDataFromYoutubeApi():
    url = 'https://youtube.googleapis.com/youtube/v3/search'

    active_api_key = getApiKey()
    
    if active_api_key:
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
            'key': active_api_key.api_key,
            'pageToken': details.page_token
        })

        response = response.json()

        if 'error' in response:
            if response['error']['code'] == 403:
                print('error')
                # Get a list of reasons why the request failed
                reasons = [error['reason'] for error in response['error']['errors']]
                if 'quotaExceeded' in reasons:
                    active_api_key.exhausted_on = datetime.datetime.now(datetime.timezone.utc)
                    active_api_key.save()
                    active_api_key = getApiKey()
            print(f'Unexpected Response obtained. Take a look ===> {json.dumps(response)}')
            return
                
        
        if 'items' in response:
            for item in response['items']:
                published_at = utcRFC3339toDatetime(
                    item['snippet']['publishedAt'])

                # Reject entries which are older than the minimum time
                if published_at < details.published_after:
                    break

                saveYoutubeVideoFromJson(item)
            
            if not response['items']:
                print('No results obtained for this request')
        else:
            print(f'Unexpected Response obtained. Take a look ===> {json.dumps(response)}')
                
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

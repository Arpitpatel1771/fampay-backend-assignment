import json
import math
import datetime
from django.http import JsonResponse
from django.shortcuts import render

from Ingestor.models import YoutubeVideo, RequestDetails, Keys
from Index.index import Index
from Ingestor.util import serializeYoutubeVideoToJson
def get_now():
    return datetime.datetime.now(datetime.timezone.utc)

# Create your views here.
def get_all_videos(request):
    try:
        # query params
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 20))
        filter = str(request.GET.get('filter', ''))
        order_by = str(request.GET.get('orderBy', ''))
        order_direction = str(request.GET.get('orderDirection', ''))
        
        # sanitize params
        if not page or page < 1:
            page = 1
        
        if order_direction == 'desc':
            # using '-' here so that it can be added directly instead of using if cases
            # e.g. descending title -> order_by(f'{order_direction}title') -> order_by('-title')
            order_direction = '-'
        else:
            order_direction = ''
        
        # generate queryset
        queryset = YoutubeVideo.objects.all()
        
        # apply filter
        if filter == 'day':
            queryset = queryset.filter(published_at__day=get_now().day)
        elif filter == 'month':
            queryset = queryset.filter(published_at__month=get_now().month)
        elif filter == 'year':
            queryset = queryset.filter(published_at__year=get_now().year)
        
        # apply order by
        if order_by == 'date':
            queryset = queryset.order_by(f'{order_direction}published_at')
        elif order_by == 'title':
            queryset = queryset.order_by(f'{order_direction}title')
        elif order_by == 'channel':
            queryset = queryset.order_by(f'{order_direction}channel_title')
        else:
            queryset = queryset.order_by('-id')
        
        # paginate the queryset
        queryset = queryset[(page - 1) * size: page * size]
        
        # generate response list
        video_data = []
        
        for video in queryset:
            video_data.append(serializeYoutubeVideoToJson(video))
        
        return JsonResponse({
            'responseCode': 200,
            'responseMessage': 'Success',
            'totalPages': math.ceil(YoutubeVideo.objects.all().order_by('-published_at').count()/size),
            'payload': video_data
        })
        
    except Exception as exc:
        print(f'Exception Occured in list api of Landing Page ===> {str(exc)}')
        return JsonResponse({
            'responseCode': 500,
            'responseMessage': 'Error <<500>>: Internal Server Error'
        })

def search_videos(request):
    try:
        # query params
        query = str(request.GET.get('query', ''))
        
        if len(query) < 1:
            return JsonResponse({
                'responseCode': 400,
                'responseMessage': 'Error <<400>>: Query string should be atleast 1 characters long'
            })
        
        results = Index().search(query=query)
        
        return JsonResponse({
            'responseCode': 200,
            'responseMessage': 'Success',
            'payload': results
        })
        
    except Exception as exc:
        print(f'Exception Occured in search api of Landing Page ===> {str(exc)}')
        return JsonResponse({
            'responseCode': 500,
            'responseMessage': 'Error <<500>>: Internal Server Error'
        })

def change_request_details(request):
    try:
        query = str(request.GET.get('query',''))
        
        if len(query) < 1:
            return JsonResponse({
                'responseCode': 400,
                'responseMessage': 'Error <<400>>: Query string should be atleast 1 characters long'
            })
        
        request_details = RequestDetails.objects.last()
        request_details.query = query
        request_details.save()
        
        return JsonResponse({
            'responseCode': 200,
            'responseMessage': 'Success'
        })
        
    except Exception as exc:
        print(f'Exception Occured in change request details api of Landing Page ===> {str(exc)}')
        return JsonResponse({
            'responseCode': 500,
            'responseMessage': 'Error <<500>>: Internal Server Error'
        })

def add_api_keys(request):
    try:
        # query params
        keys = request.GET.get('keys','').split(',')

        # sanitize inputs
        keys = [str(key).strip() for key in keys]

        for key in keys:
            Keys.objects.create(api_key=key, exhausted_on=None)
            
        return JsonResponse({
            'responseCode': 200,
            'responseMessage': 'Success'
        })
    
    except Exception as exc:
        print(f'Exception Occured in list api of Landing Page ===> {str(exc)}')
        return JsonResponse({
            'responseCode': 500,
            'responseMessage': 'Error <<500>>: Internal Server Error'
        })
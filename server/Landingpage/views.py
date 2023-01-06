import json
from django.http import JsonResponse
from django.shortcuts import render

from Ingestor.models import YoutubeVideo, RequestDetails
from Index.index import Index

# Create your views here.
def get_all_videos(request):
    try:
        # query params
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 20))
        
        # sanitize params
        if not page or page < 1:
            page = 1
        
        video_data = list(YoutubeVideo.objects.all().order_by('-published_at').values(
            'video_id', 'published_at', 'channel_id','title', 'description','thumbnail', 'channel_title'))[(page - 1) * size: page * size]
        
        return JsonResponse({
            'responseCode': 200,
            'responseMessage': 'Success',
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
        print(f'Exception Occured in list api of Landing Page ===> {str(exc)}')
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
        print(f'Exception Occured in list api of Landing Page ===> {str(exc)}')
        return JsonResponse({
            'responseCode': 500,
            'responseMessage': 'Error <<500>>: Internal Server Error'
        })
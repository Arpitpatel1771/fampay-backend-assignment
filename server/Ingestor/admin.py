from django.contrib import admin
from Ingestor.models import *
# Register your models here.

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = [
        'video_id',
        'title',
        'description',
        'channel_id',
        'channel_title',
        'published_at',
        'thumbnail',
        'raw_data'
    ]
    
    search_fields = [
        'id',
        'video_id',
        'title'
    ]
    
    list_filter = [
        'channel_title',
        'channel_id'
    ]
    
    

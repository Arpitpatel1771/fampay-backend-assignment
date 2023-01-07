from django.db import models

# Create your models here.
class YoutubeVideo(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    published_at = models.DateTimeField()
    channel_id = models.CharField(max_length=75)
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.URLField(null=True)
    channel_title = models.CharField(max_length=250, null=True)
    raw_data = models.JSONField(null=True)
    
    def __str__(self):
        return f'{self.video_id} -> {self.title}'
    
    def save(self, *args, **kwargs):
        super(YoutubeVideo, self).save(*args, **kwargs)
        from Index.index import Index
        Index().addObjectToIndex(self)
        
class Keys(models.Model):
    api_key = models.CharField(max_length=300, unique=True)
    exhausted_on = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.api_key}: exhausted_on -> {str(self.exhausted_on)}'

class RequestDetails(models.Model):
    query = models.TextField()
    published_after = models.DateTimeField()
    page_token = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'query -{self.query}, published_after - {str(self.published_after)}'
    
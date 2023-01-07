import datetime
from Ingestor.models import YoutubeVideo

def get_now():
    return datetime.datetime.now(datetime.timezone.utc)

def utcDatetimeToRFC3339(datetime_obj: datetime.datetime) -> str:
    # Removing the +00:00 at the end and adding a Z at the end
    # Google's API was not working without the Z
    return datetime_obj.isoformat().split('+')[0] + 'Z'


def utcRFC3339toDatetime(str: str) -> datetime.datetime:
    # Removing the Z at the end and adding +00:00
    # datetime.fromisoformat was not working without the +00:00
    return datetime.datetime.fromisoformat(str.split('Z')[0] + '+00:00')


def saveYoutubeVideoFromJson(dictionary: dict):
    '''
    Create a YoutubeVideo object from the response JSON recieved from the Youtube API
    '''
    video_id = dictionary['id']['videoId']
    if YoutubeVideo.objects.filter(video_id=video_id).exists():
        return

    YoutubeVideo.objects.create(
        video_id=video_id,
        published_at=utcRFC3339toDatetime(
            dictionary['snippet']['publishedAt']),
        channel_id=dictionary['snippet']['channelId'],
        title=dictionary['snippet']['title'],
        description=dictionary['snippet']['description'],
        thumbnail=dictionary['snippet']['thumbnails']['medium']['url'],
        channel_title=dictionary['snippet']['channelTitle'],
        raw_data=dictionary
    )

def serializeYoutubeVideoToJson(youtubevideo: YoutubeVideo):
    
    data = {
        'video_id': youtubevideo.video_id,
        'channel_id': youtubevideo.channel_id,
        'title': youtubevideo.title,
        'description': youtubevideo.description,
        'thumbnail': youtubevideo.thumbnail,
        'channel_title': youtubevideo.channel_title,
        'published_at': youtubevideo.published_at,
    }
    
    # Get time difference string
    # i.e. "Uploaded 2 months ago" or "Uploaded Just Now"
    published_at = youtubevideo.published_at
    now = get_now()
    published_info = ''
    if published_at.year != now.year:
        timedelta = now.year - published_at.year
        time_metric = 'years' if timedelta > 1 else 'year'
    elif published_at.month != now.month:
        timedelta = now.month - published_at.month
        time_metric = 'months' if timedelta > 1 else 'month'
    elif published_at.day != now.day:
        timedelta = now.day - published_at.day
        time_metric = 'days' if timedelta > 1 else 'day'
    elif published_at.hour != now.hour:
        timedelta = now.hour - published_at.hour
        time_metric = 'hours' if timedelta > 1 else 'hour'
    elif published_at.minute != now.minute:
        timedelta = now.minute - published_at.minute
        time_metric = 'minutes' if timedelta > 1 else 'minute'
    elif published_at.second != now.second:
        timedelta = now.second - published_at.second
        time_metric = 'seconds' if timedelta > 1 else 'second'
    else:
        published_info = 'Uploaded Just Now'
        
    if published_info == '':
        published_info = f'Uploaded {timedelta} {time_metric} ago'
    
    data['published_info'] = published_info
    
    return data
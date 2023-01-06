import datetime
from Ingestor.models import YoutubeVideo


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
    json_object = {
        "video_id": youtubevideo.video_id,
        "published_at": youtubevideo.published_at,
        "channel_id": youtubevideo.channel_id,
        "title": youtubevideo.title,
        "description": youtubevideo.description,
        "thumbnail": youtubevideo.thumbnail,
        "channel_title": youtubevideo.channel_title
    }
    
    return json_object
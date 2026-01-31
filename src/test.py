import pandas as pd
import requests
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
from google_play_scraper import reviews, Sort

def fetch_youtube_no_api(url, limit=30):
    try:
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT)
        data = []
        for i, c in enumerate(comments):
            if i >= limit: 
                break
            data.append({"Author": c.get('author'), "Content": c.get('text')})
        return pd.DataFrame(data)
    except Exception as e:
        return pd.DataFrame()

def fetch_youtube_api(video_id, api_key, limit=50):
    comments = []
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': api_key,
        'maxResults': limit,
        'textFormat': 'plainText'
    }
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            for item in res.json().get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'Author': snippet['authorDisplayName'],
                    'Content': snippet['textDisplay']
                })
    except:
        pass
    return pd.DataFrame(comments)

def fetch_playstore(app_id, limit=50):
    try:
        result, _ = reviews(app_id, lang='id', country='id', sort=Sort.NEWEST, count=limit)
        if result:
            df = pd.DataFrame(result)
            return df[['userName', 'content']].rename(columns={'userName': 'Author', 'content': 'Content'})
    except:
        return pd.DataFrame()
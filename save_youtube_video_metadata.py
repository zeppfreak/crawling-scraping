import os
import logging
from typing import Iterator, List

from apiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def main():
    mongo_client = MongoClient('localhost', 27017)
    collection = mongo_client.youtube.videos

    for items_per_page in search_videos('手芸'):
        save_to_mongodb(collection, items_per_page)
    
    show_top_videos(collection)


def search_videos(query: str, max_pages: int=5, apiclient=None) -> Iterator[List[dict]]:
    if apiclient is None:
        apiclient = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    search_request = apiclient.search().list(
        part='id',
        q=query,
        type='video',
        maxResults=50,
    )

    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute()
        video_ids = [item['id']['videoId'] for item in search_response['items']]

        videos_response = apiclient.videos().list(
            part='snippet, statistics',
            id=','.join(video_ids)
        ).execute()

        yield videos_response['items']

        search_request = apiclient.search().list_next(search_request, search_response)
        i += 1


def save_to_mongodb(collection: Collection, items: List[dict]):
    for item in items:
        item['_id'] = item['id']

        for key, value in item['statistics'].items():
            item['statistics'][key] = int(value)
    
    operations = [ReplaceOne({'_id': item['_id']}, item, upsert=True) for item in items]
    result = collection.bulk_write(operations)
    logging.info(f'Upserted {result.upserted_count} documents.')


def save_to_mongodb_batch(collection: Collection, items: List[dict], batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        batch_items = items[i:i+batch_size]
        for item in batch_items:
            item['_id'] = item['id']

            for key, value in item['statistics'].items():
                item['statistics'][key] = int(value)
        
        operations = [ReplaceOne({'_id': item['_id']}, item, upsert=True)for item in batch_items]
        result = collection.bulk_write(operations)
        logging.info(f'Upserted {result.upserted_count} documents.')

def show_top_videos(collection: Collection):
    for item in collection.find().sort('statistics.viewCount', DESCENDING).limit(5):
        print(item['statistics']['viewCount'], item['snippet']['title'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()




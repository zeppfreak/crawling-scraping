import unittest
from unittest.mock import MagicMock
from pymongo.collection import Collection
from pymongo.results import BulkWriteResult
from typing import List
from save_youtube_video_metadata import search_videos, save_to_mongodb


class TestSaveYoutubeVideoMetadata(unittest.TestCase):
    def test_search_videos(self):
        # YouTube APIのモックを作成する
        youtube = MagicMock()
        youtube.search().list().execute.return_value = {
            'items': [
                {'id': {'videoId': 'id1'}},
                {'id': {'videoId': 'id2'}},
            ]
        }
        youtube.videos().list().execute.return_value = {
            'items': [
                {'id': 'id1', 'statistics': {'viewCount': '1000'}, 'snippet': {'title': 'Title 1'}},
                {'id': 'id2', 'statistics': {'viewCount': '2000'}, 'snippet': {'title': 'Title 2'}}
            ]
        }

        # 検索結果のアイテムを取得する
        items_per_page = next(search_videos('test', max_pages=1, apiclient=youtube))

        # 検索結果のアイテムが正しいかどうかを確認する
        self.assertEqual(len(items_per_page), 2)
        self.assertEqual(items_per_page[0]['id'], 'id1')
        self.assertEqual(items_per_page[0]['statistics']['viewCount'], '1000')
        self.assertEqual(items_per_page[0]['snippet']['title'], 'Title 1')
        self.assertEqual(items_per_page[1]['id'], 'id2')
        self.assertEqual(items_per_page[1]['statistics']['viewCount'], '2000')
        self.assertEqual(items_per_page[1]['snippet']['title'], 'Title 2')


    def test_save_to_mongodb(self):
        # MongoDBのコレクションのモックを作成する
        collection = MagicMock(Collection)
        bulk_write_result = MagicMock(BulkWriteResult)
        collection.bulk_write.return_value = bulk_write_result

        # MongoDBに保存するアイテムを作成する
        items = [
            {'id': 'id1', 'statistics': {'viewCount': '1000'}, 'snippet': {'title': 'Title 1'}},
            {'id': 'id2', 'statistics': {'viewCount': '2000'}, 'snippet': {'title': 'Title 2'}}
        ]

        # MongoDBに保存するアイテムを保存する
        save_to_mongodb(collection, items)

        # MongoDBに保存されたアイテムが正しいかどうかを確認する
        collection.bulk_write.assert_called_once()
        bulk_write_result.upserted_count == 2
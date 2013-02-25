# coding: utf-8
import hashlib

import memcache
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen
from asyncdynamo.orm.table import Table

from mybookmarks import settings

import logging


class BookmarkSaveHandler(RequestHandler):

    def initialize(self, *args, **kwargs):
        conf = getattr(settings, 'MEMCACHE', dict())
        self.cache = memcache.Client(**conf)

    @addslash
    @gen.engine
    @asynchronous
    def post(self, user_id):
        """
        Save a new user bookmark

         - userid: user id
        """
        title = self.get_argument('title')
        url = self.get_argument('url')

        cache_key = hashlib.sha1(user_id).hexdigest()
        user_data = self.cache.get(cache_key)

        if not user_data:
            table = Table('User', key='id')
            item = yield gen.Task(table.get_item,
                {'HashKeyElement': {'S': user_id}})

            if 'Item' not in item:
                self.write({'status': '', 'error': 'user not found'})
                self.finish()
                return

            self.cache.set(cache_key, user_data)

        bookmarks = Table('Bookmark', key='id')

        bookmark_id = ":".join(user_data['id'], url)
        bookmark_data = {
            'id': {"S": bookmark_id},
            'user_id': {"S": user_id},
            'title': {"S": title},
            'url': {"S": url},
        }
        item_saved = yield gen.Task(bookmarks.put_item, bookmark_data)

        if item_saved and 'ConsumedCapacityUnits' in item_saved:
            response = {'status': 'OK', 'bookmark': bookmark_data}
        else:
            logging.error('bookmark not saved %s' % item_saved)
            response = {'status': '', 'error': 'unknown error'}

        self.write(response)
        self.finish()

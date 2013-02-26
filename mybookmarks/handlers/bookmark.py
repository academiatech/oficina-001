# coding: utf-8
import hashlib
import memcache
import logging

from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen

from asyncdynamo.orm.session import Session
from asyncdynamo.orm.table import Table

from mybookmarks import settings


class BookmarkHandler(RequestHandler):

    def initialize(self, *args, **kwargs):
        conf = getattr(settings, 'MEMCACHE', dict())
        self.cache = memcache.Client(**conf)
        self.session = Session()

    @addslash
    @gen.engine
    @asynchronous
    def get(self, user_id):
        """
        Get user bookmarks

         - userid: user id
        """
        
        query_dict = {'user_id': {'S': user_id}}

        item = yield gen.Task(self.session.query, 
            'Bookmark', query_dict)

        print '----------------------'
        print item

        if 'Item' not in item:
            self.write({'status': '', 'error': 'user not found'})
            self.finish()
            return

        user_data = {
            'id': item['Item']['id']['S'],
            'name': item['Item']['name']['S'],
            'email': item['Item']['email']['S']
        }

        self.cache.set(cache_key, user_data)

        self.write({'status': 'OK', 'user': user_data})
        self.finish()

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

            user_data = item.get('Item')
            self.cache.set(cache_key, user_data)
            
        bookmarks = Table('Bookmark', key='id')

        bookmark_id = ":".join([user_data['id']['S'], url])
        bookmark_data = {
            'id': {"S": bookmark_id},
            'user_id': {"S": user_id},
            'title': {"S": title},
            'url': {"S": url},
        }
        item_saved = yield gen.Task(bookmarks.put_item, bookmark_data)

        saved_data = {
            'id': bookmark_id,
            'user_id': user_id,
            'title': title,
            'url': url
        }

        if item_saved and 'ConsumedCapacityUnits' in item_saved:
            response = {'status': 'OK', 'bookmark': saved_data}
        else:
            logging.error('bookmark not saved %s' % item_saved)
            response = {'status': '', 'error': 'unknown error'}

        self.write(response)
        self.finish()

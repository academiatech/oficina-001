# coding: utf-8
import hashlib

import memcache
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen
from asyncdynamo.orm.table import Table

from mybookmarks import settings
from mybookmarks.handlers import jsonp

import logging


class BookmarkSaveHandler(RequestHandler):

    def initialize(self, *args, **kwargs):
        conf = getattr(settings, 'MEMCACHE', dict())
        self.cache = memcache.Client(**conf)

    @addslash
    @jsonp
    @gen.engine
    @asynchronous
    def get(self, user_id, callback):
        """
        get user preference

         - userid: user id
        """
        cache_key = hashlib.sha1(user_id).hexdigest()
        user_data = self.cache.get(cache_key)

        if not user_data:
            table = Table('User', key='id')
            item = yield gen.Task(table.get_item,
                {'HashKeyElement': {'S': user_id}})

            if 'Item' not in item:
                callback({'status': '', 'error': 'user not found'})
                return

            user_data = {
                'user_id': item['Item']['user_id']['S'],
            }

            self.cache.set(cache_key, user_data)

        callback({'status': 'OK', 'user': user_data})

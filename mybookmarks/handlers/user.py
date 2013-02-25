# coding: utf-8
import hashlib
import uuid

import memcache
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen
from asyncdynamo.orm.table import Table

from mybookmarks import settings
from mybookmarks.handlers import jsonp

import logging


class UserHandler(RequestHandler):

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
                'name': item['Item']['name']['S'],
                'email': item['Item']['email']['S']
            }

            self.cache.set(cache_key, user_data)

        callback({'status': 'OK', 'user': user_data})


class UserSaveHandler(RequestHandler):

    @addslash
    @jsonp
    @gen.engine
    @asynchronous
    def post(self, callback):
        """
        save user data

         - name: user name
         - email: user email
        """

        name = self.get_argument('name')
        email = self.get_argument('email')
        user_id = uuid.uuid5(uuid.NAMESPACE_OID, email)

        table = Table('User', key='id')
        item = yield gen.Task(table.get_item,
            {'HashKeyElement': {'S': user_id}})

        if 'Item' in item:
            callback({'status': '', 'error': 'user already exist'})
            return

        user_data = {
            'id': {"S": user_id},
            'name': {"S": name},
            'email': {"S": email},
        }

        table = Table('User', key='id')

        item_saved = yield gen.Task(table.put_item, user_data)
        saved_data = {
            'user_id': user_id,
            'name': name,
            'email': email
        }

        cache_key = hashlib.sha1(user_id).hexdigest()
        self.cache.set(cache_key, saved_data)

        if item_saved and 'ConsumedCapacityUnits' in item_saved:
            response = {'status': 'OK', 'user': saved_data}
        else:
            logging.error('user not saved %s' % item_saved)
            response = {'status': '', 'error': 'unknown error'}

        callback(response)

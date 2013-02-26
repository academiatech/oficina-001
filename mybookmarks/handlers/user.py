# coding: utf-8
import hashlib
import uuid

import memcache
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen
from asyncdynamo.orm.table import Table

from mybookmarks import settings

import logging


class UserHandler(RequestHandler):

    def initialize(self, *args, **kwargs):
        conf = getattr(settings, 'MEMCACHE', dict())
        self.cache = memcache.Client(**conf)

    @addslash
    @gen.engine
    @asynchronous
    def get(self, user_id):
        """
        Get user

         - userid: user id
        """
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

            user_data = {
                'id': item['Item']['id']['S'],
                'name': item['Item']['name']['S'],
                'email': item['Item']['email']['S']
            }

            self.cache.set(cache_key, user_data)

        self.write({'status': 'OK', 'user': user_data})
        self.finish()


class UserSaveHandler(RequestHandler):

    def initialize(self, *args, **kwargs):
        conf = getattr(settings, 'MEMCACHE', dict())
        self.cache = memcache.Client(**conf)

    @addslash
    @gen.engine
    @asynchronous
    def post(self):
        """
        Create new user

         - name: user name
         - email: user email
        """

        name = self.get_argument('name')
        email = self.get_argument('email')

        user_id = str(uuid.uuid5(uuid.NAMESPACE_OID, email.encode('utf-8')))

        table = Table('User', key='id')
        item = yield gen.Task(table.get_item,
            {'HashKeyElement': {'S': user_id}})

        if 'Item' in item:
            self.write({'status': '', 'error': 'user already exist'})
            self.finish()
            return

        user_data = {
            'id': {"S": user_id},
            'name': {"S": name},
            'email': {"S": email},
        }

        table = Table('User', key='id')

        item_saved = yield gen.Task(table.put_item, user_data)
        saved_data = {
            'id': user_id,
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

        self.write(response)
        self.finish()

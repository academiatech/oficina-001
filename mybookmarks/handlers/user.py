# coding: utf-8
import hashlib
import uuid

import memcache
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen
from asyncdynamo.orm.table import Table

from mybookmarks.models.user import User
from mybookmarks import settings

import logging


class UserHandler(RequestHandler):

    @addslash
    @gen.engine
    @asynchronous
    def get(self, user_id):
        """
        Get user

         - userid: user id
        """
        user = yield gen.Task(User.get, user_id)
        if not user:
            self.write({'status': '', 'error': 'user not found'})
            self.finish()
            return

        self.write({'status': 'OK', 'user': user})
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

        UserTable = Table('User', key='id')
        item = yield gen.Task(UserTable.get_item,
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
        item_saved = yield gen.Task(UserTable.put_item, user_data)
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

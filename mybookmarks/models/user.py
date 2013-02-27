import hashlib
import memcache
import logging
from tornado import gen

from mybookmarks.tables import UserTable
from mybookmarks import settings

cache = memcache.Client(**getattr(settings, 'MEMCACHE', dict()))


class User(object):

    @staticmethod
    @gen.engine
    def get(user_id, callback):
        cache_key = hashlib.sha1(user_id).hexdigest()
        user_data = cache.get(cache_key)

        if not user_data:
            logging.debug('getting user from table...')
            userTable = UserTable()
            item = yield gen.Task(userTable.get_item,
                {'HashKeyElement': {'S': user_id}})
            logging.debug('get user from table')

            if 'Item' in item:
                user_data = {
                    'id': item['Item']['id']['S'],
                    'name': item['Item']['name']['S'],
                    'email': item['Item']['email']['S']
                }
                logging.debug('putting user in cache')
                cache.set(cache_key, user_data)
        else:
            logging.debug('getting user from cache')

        callback(user_data)

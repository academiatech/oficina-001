import hashlib
import memcache
from tornado import gen

from mybookmarks.tables import UserTable
from mybookmarks import settings


class User(object):

    @staticmethod
    @gen.engine
    def get(user_id, callback):
        conf = getattr(settings, 'MEMCACHE', dict())
        cache = memcache.Client(**conf)

        cache_key = hashlib.sha1(user_id).hexdigest()
        user_data = cache.get(cache_key)

        if not user_data:
            userTable = UserTable()
            item = yield gen.Task(userTable.get_item,
                {'HashKeyElement': {'S': user_id}})

            if 'Item' in item:
                user_data = {
                    'id': item['Item']['id']['S'],
                    'name': item['Item']['name']['S'],
                    'email': item['Item']['email']['S']
                }
                cache.set(cache_key, user_data)

        callback(user_data)

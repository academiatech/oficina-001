# coding: utf-8
import logging
import uuid
import time
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen

from mybookmarks.tables import BookmarkTable

from mybookmarks.models.user import User


class BookmarkHandler(RequestHandler):

    @addslash
    @gen.engine
    @asynchronous
    def get(self, user_id):
        """
        Get user bookmarks

         - userid: user id
        """
        user = yield gen.Task(User.get, user_id)
        if not user:
            self.write({'status': '', 'error': 'user not found'})
            self.finish()
            return

        bookmarkTable = BookmarkTable()

        bookmarks = yield gen.Task(bookmarkTable.query,
            hash_key_value={'S': user_id},
            limit=10)

        response = {'status': 'OK', 'total': bookmarks['Count'], 'bookmarks': []}

        for bookmark in bookmarks['Items']:
            response['bookmarks'].append({
                'user_id': bookmark['user_id']['S'],
                'url': bookmark['url']['S'],
                'title': bookmark['title']['S'],
                'created': bookmark['created']['N'],
            })

        self.write(response)
        self.finish()

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

        user = yield gen.Task(User.get, user_id)
        if not user:
            self.write({'status': '', 'error': 'user not found'})
            self.finish()
            return

        bookmarkTable = BookmarkTable()

        bookmark_data = {
            'user_id': {"S": user_id},
            'title': {"S": title},
            'url': {"S": url},
            'created': {"N": str(int(time.time()))},
        }
        item_saved = yield gen.Task(bookmarkTable.put_item, bookmark_data)

        saved_data = {
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

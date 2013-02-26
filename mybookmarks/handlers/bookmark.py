# coding: utf-8
import hashlib
import logging
import uuid
from tornado.web import addslash, asynchronous, RequestHandler
from tornado import gen

from asyncdynamo.orm.session import Session
from asyncdynamo.orm.table import Table

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
        query_dict = {'user_id': {'S': user_id}}
        session = Session()

        item = yield gen.Task(session.query,
            'Bookmark', query_dict)

        if 'Item' not in item:
            self.write({'status': '', 'error': 'user not found'})
            self.finish()
            return

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

        bookmarks = Table('Bookmark', key='id')

        bookmark_id = str(uuid.uuid5(uuid.NAMESPACE_OID, ":".join([user['id'], url]).encode('utf-8')))
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

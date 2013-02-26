import json
import uuid
import time
from mybookmarks.server import application
from mybookmarks.tables import UserTable, BookmarkTable

from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from urllib import urlencode


class BookmarkTestCase(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return application

    def tearDown(self):
        user = UserTable()
        user.drop(callback=self.stop)

        bookmark = BookmarkTable()
        bookmark.drop(callback=self.stop)

        self.wait()

    def test_create_bookmark(self):

        user_data = {
            'id': {'S': 'user-id'},
            'name': {'S': 'should be user name'},
            'email': {'S': 'shouldbe@user.email'}
        }
        userTable = UserTable()
        userTable.put_item(user_data, callback=self.stop)
        self.wait()

        params = urlencode({
            'title': 'should be book title',
            'url': 'http://academiatech.com.br/'
        })

        resource = '/users/user-id/bookmarks/'
        self.http_client.fetch(self.get_url(resource), method='POST',
            body=params, callback=self.stop)

        response = self.wait()

        self.assertEquals(200, response.code)

        response_data = json.loads(response.body)
        self.assertEquals('OK', response_data['status'])
        self.assertEquals('http://academiatech.com.br/', response_data['bookmark']['url'])

    def test_get_bookmarks(self):
        user_id = str(uuid.uuid4())

        user_data = {
            'id': {'S': user_id},
            'name': {'S': 'should be user name'},
            'email': {'S': 'shouldbe@user.email'}
        }
        userTable = UserTable()
        userTable.put_item(user_data, callback=self.stop)
        self.wait()

        bookmarks = [{
            'user_id': {'S': user_id},
            'created': {'N': str(int(time.time()))},
            'url': {'S': 'http://wikipedia.org'},
            'title': {'S': 'wikipedia'}
        }, {
            'user_id': {'S': user_id},
            'created': {'N': str(int(time.time()))},
            'url': {'S': 'http://academiatech.com.br'},
            'title': {'S': 'academia tech'}
        }]
        bookmarkTable = BookmarkTable()

        for bookmark in bookmarks:
            bookmarkTable.put_item(bookmark, callback=self.stop)
            self.wait()

        resource = '/users/{}/bookmarks/'.format(user_id)
        self.http_client.fetch(self.get_url(resource), callback=self.stop)
        response = self.wait()

        self.assertEquals(200, response.code)

        response_data = json.loads(response.body)
        self.assertEquals('OK', response_data['status'])
        self.assertEquals(2, response_data['total'])

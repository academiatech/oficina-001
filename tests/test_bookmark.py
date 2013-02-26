import json
import uuid
from mybookmarks.server import application

from asyncdynamo.orm.table import Table
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from urllib import urlencode


class BookmarkTestCase(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return application

    def tearDown(self):
        user = Table('User', key='id')
        user.drop(callback=self.stop)

        bookmark = Table('Bookmark', key='id')
        bookmark.drop(callback=self.stop)

        self.wait()

    def test_create_bookmark(self):

        user_data = {
            'id': {'S': 'user-id'},
            'name': {'S': 'should be user name'},
            'email': {'S': 'shouldbe@user.email'}
        }
        UserTable = Table('User', key='id')
        UserTable.put_item(user_data, callback=self.stop)
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
        bookmark_id = str(uuid.uuid4())

        user_data = {
            'id': {'S': user_id},
            'name': {'S': 'should be user name'},
            'email': {'S': 'shouldbe@user.email'}
        }
        UserTable = Table('User', key='id')
        UserTable.put_item(user_data, callback=self.stop)
        self.wait()

        bookmark_data = {
            'id': {'S': bookmark_id},
            'user_id': {'S': user_id},
            'url': {'S': 'http://academiatech.com.br'},
            'title': {'S': 'academia tech'}
        }
        BookmarkTable = Table('Bookmark', key='id')
        BookmarkTable.put_item(bookmark_data, callback=self.stop)
        self.wait()

        resource = '/users/{}/bookmarks/'.format(user_id)
        self.http_client.fetch(self.get_url(resource), callback=self.stop)
        response = self.wait()

        print response.body
        self.assertEquals(200, response.code)

import json

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
            'id': 'user-id',
            'name': 'should be user name',
            'email': 'shouldbe@user.email'
        }
        UserTable = Table('User', key='id')
        UserTable.put_item(user_data, callback=self.stop)
        item_saved = self.wait()

        params = urlencode({
            'title': 'should be book title',
            'url': 'http://academiatech.com.br/'
        })

        resource = '/users/{}/bookmark/'.format(user_data['id'])
        self.http_client.fetch(self.get_url(resource), method='POST',
            body=params, callback=self.stop)

        response = self.wait()

        self.assertEquals(200, response.code)

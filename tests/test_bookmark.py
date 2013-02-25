import json

from bookmark.server import application
from bookmark.handlers.bookmark import BookmarkSaveHandler

from asyncdynamo.orm.table import Table
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from fudge import patched_context
from urllib import urlencode


class BookmarkTestCase(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return application

    def tearDown(self):
        table = Table('User', key='id')
        table.drop(callback=self.stop)

        self.wait()

    def test_can_be_save_user_preferences(self):

        app_id = "shouldBeAPP_ID"
        user_id = "shouldBeUserId"
        access_token = "shouldBeAccessToken"
        share = "1"
        notify_user = "1"
        ident = ":".join([app_id, user_id])

        params = urlencode({
            'app_id': app_id,
            'user_id': user_id,
            'access_token': access_token,
            'share': share,
            'notify_user': notify_user,
        })

        def is_valid_access_token(handler, access_token, callback):
            callback(True)

        with patched_context(UserSaveHandler, "is_valid_access_token", is_valid_access_token):
            self.http_client.fetch(self.get_url('/user/save?' + params), self.stop)
            response = self.wait()

        # test handler response
        self.assertEquals('callback({"status": "OK"});', response.body)

        # test user data
        table = Table('User', key='id')
        table.get_item({'HashKeyElement': {'S':ident}}, self.stop)
        item = self.wait()

        self.assertEquals(ident, item['Item']['id']['S'])
        self.assertEquals(app_id, item['Item']['app_id']['S'])
        self.assertEquals(user_id, item['Item']['user_id']['S'])
        self.assertEquals(share, item['Item']['share']['S'])
        self.assertEquals(notify_user, item['Item']['notify_user']['S'])
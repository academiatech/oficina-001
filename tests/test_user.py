import json

from mybookmarks.server import application

from asyncdynamo.orm.table import Table
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase
from urllib import urlencode


class UserTestCase(AsyncHTTPTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def get_app(self):
        return application

    def tearDown(self):
        table = Table('User', key='id')
        table.drop(callback=self.stop)

        self.wait()

    def test_create_user(self):
        params = urlencode({
            'name': 'should be user name',
            'email': 'should be email name'
        })

        self.http_client.fetch(self.get_url('/users/'), method='POST',
            body=params, callback=self.stop)

        response = self.wait()

        self.assertEquals(200, response.code)

        response_data = json.loads(response.body)

        self.assertEquals('OK', response_data['status'])
        self.assertEquals(u'cf685fe8-1ea0-52ca-af49-c6cdc023b2a0',
            response_data['user']['id'])
        self.assertEquals(u'should be user name',
            response_data['user']['name'])
        self.assertEquals(u'should be email name',
            response_data['user']['email'])

    def test_create_user_bad_request(self):
        params = urlencode({
            'name': 'should be user name',
        })

        self.http_client.fetch(self.get_url('/users/'), method='POST',
            body=params, callback=self.stop)

        response = self.wait()
        self.assertEquals(400, response.code)

    def test_get_user(self):
        params = urlencode({
            'name': 'should be user name',
            'email': 'should be email name'
        })

        self.http_client.fetch(self.get_url('/users/'), method='POST',
            body=params, callback=self.stop)

        response = self.wait()
        response_data = json.loads(response.body)

        user_id = response_data['user']['id']

        self.http_client.fetch(self.get_url('/users/{}/'.format(user_id)),
            callback=self.stop)
        response = self.wait()

        self.assertEquals(200, response.code)
        response_data = json.loads(response.body)

        self.assertEquals('should be user name', response_data['user']['name'])

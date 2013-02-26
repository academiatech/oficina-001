# coding: utf-8
from tornado.web import URLSpec

from mybookmarks.handlers.home import HomeHandler
from mybookmarks.handlers.user import UserHandler, UserSaveHandler
from mybookmarks.handlers.bookmark import BookmarkHandler, BookmarkSaveHandler

urls = (
    URLSpec(r'/', HomeHandler, name='home'),
    URLSpec(r'/users/?', UserSaveHandler, name='users.save'),
    URLSpec(r'/users/(?P<user_id>[^/]+)/?', UserHandler,
        name='users.get'),
    URLSpec(r'/users/(?P<user_id>[^/]*)/bookmark/new/?', BookmarkSaveHandler,
        name='bookmark.save'),
    URLSpec(r'/users/(?P<user_id>[^/]*)/bookmark/?', BookmarkHandler,
    	name='bookmark.get'),
)

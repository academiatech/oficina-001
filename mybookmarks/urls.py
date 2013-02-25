# coding: utf-8
from tornado.web import URLSpec

from mybookmarks.handlers.home import HomeHandler
from mybookmarks.handlers.user import UserHandler, UserSaveHandler
from mybookmarks.handlers.bookmark import BookmarkSaveHandler

uuid_regexp = "[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-(:?8|9|A|B)[a-f0-9]{3}-[a-f0-9]{12}"

urls = (
    URLSpec(r'/', HomeHandler, name='home'),
    URLSpec(r'/users/?'.format(uuid_regexp), UserHandler, name='users.get'),
    URLSpec(r'/users/{}/?'.format(uuid_regexp), UserSaveHandler,
        name='users.save'),
    URLSpec(r'/users/{}/bookmark/?'.format(uuid_regexp), BookmarkSaveHandler,
        name='bookmark.save'),
)

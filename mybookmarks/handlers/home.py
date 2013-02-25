# coding: utf-8
from tornado.web import asynchronous, RequestHandler


class HomeHandler(RequestHandler):
    @asynchronous
    def get(self):
        title = self.get_argument('title', "Default Title")
        self.render("index.html", title=title)

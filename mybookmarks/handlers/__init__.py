from functools import wraps
import json

from tornado import gen


def jsonp(fn):
    @wraps(fn)
    @gen.engine
    def jsonp_wrap(handler, *args, **kw):
        callback_name = handler.get_argument('callback', 'callback')

        response = yield gen.Task(fn, handler, *args, **kw)

        handler.set_header("Content-Type", "application/javascript; charset=UTF-8")
        handler.write("%s(%s);" % (callback_name, json.dumps(response)))
        handler.finish()

    return jsonp_wrap

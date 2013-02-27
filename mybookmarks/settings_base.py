import os
from functools import partial


get_path_to = partial(os.path.join, os.path.dirname(__file__))

DEBUG = False

TEMPLATE_PATH = get_path_to("templates")
STATIC_PATH = get_path_to("static")

AWS_ACCESS_KEY = 'AKIAIIDHBXCO5Q543I3A'
AWS_SECRET_ACCESS_KEY = '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'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'NOTSET',
        'handlers': ['console'],
    },
    'formatters': {
        'detailed': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
}

MEMCACHE = {
    'servers': ('localhost:11211',),
    'socket_timeout': 1,
}

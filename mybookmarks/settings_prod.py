from settings_base import *

PORT = 8888

LOGGING['root']['handlers'] = ['file']
LOGGING['handlers']['file'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'formatter': 'detailed',
    'filename': '/var/log/mybookmarks/app.log',
    'encoding': 'utf-8',
}

MEMCACHE = {
    'servers': ('mybookmarks.3dpyc9.cfg.use1.cache.amazonaws.com:11211',),
    'socket_timeout': 1,
}

from settings_base import *

LOGGING['root']['handlers'] = ['file']
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'formatter': 'detailed',
    'filename': '/var/log/mybookmarks/app.log',
    'encoding': 'utf-8',
}

MEMCACHE = {
    'servers': ('mybookmarks.3dpyc9.cfg.use1.cache.amazonaws.com:11211',),
    'socket_timeout': 1,
}

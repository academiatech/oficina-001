import logging.config

from asyncdynamo.orm.session import Session

import settings


VERSION = (0, 0, 1, 'dev')

__version__ = ".".join([str(v) for v in VERSION])

logging.config.dictConfig(settings.LOGGING)

AWS_DYNAMODB_ENDPOINT = getattr(settings, 'AWS_DYNAMODB_ENDPOINT', None)
AWS_DYNAMODB_ENDPOINT_PORT = getattr(settings, 'AWS_DYNAMODB_ENDPOINT_PORT', None)
AWS_DYNAMODB_IS_SECURE = getattr(settings, 'AWS_DYNAMODB_IS_SECURE', True)
AWS_DYNAMODB_VALIDATE_CERT = getattr(settings, 'AWS_DYNAMODB_VALIDATE_CERT', True)
AWS_DYNAMODB_AUTH_REQUESTS = getattr(settings, 'AWS_DYNAMODB_AUTH_REQUESTS', True)
SESSION_DEBUG = 2 if settings.DEBUG else 0

Session.create(aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    host=AWS_DYNAMODB_ENDPOINT,
    is_secure=AWS_DYNAMODB_IS_SECURE, validate_cert=AWS_DYNAMODB_VALIDATE_CERT,
    authenticate_requests=AWS_DYNAMODB_AUTH_REQUESTS, debug=SESSION_DEBUG,
    port=AWS_DYNAMODB_ENDPOINT_PORT
)

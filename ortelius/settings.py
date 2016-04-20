
import logging
from datetime import timedelta

project_name = "ortelius"


class BaseConfig(object):
    '''Base configuration'''
    DEBUG = False
    TESTING = False
    USE_X_SENDFILE = False
    # DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://hm:hm@localhost:5432/hm"
    SQLALCHEMY_ECHO = False

    CSRF_ENABLED = True
    SECRET_KEY = "secret"  # import os; os.urandom(24)

    # LOGGING
    LOGGER_NAME = "ortelius_log"
    LOG_FILENAME = "/var/tmp/app_ortelius.log"
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"  # used by logging.Formatter

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # EMAIL CONFIGURATION
    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_MAIL_SENDER = "example@ortelius.com"

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # DEBUG_TOOLBAR = False
    # WERKZEUG_OPTS = {'host': LISTEN_HOST, 'port' : 5000}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://hm:hm@localhost:5432/hm"


class TestingConfig(BaseConfig):
    TESTING = True
    CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://hm:hm@localhost:5432/hm"
    SQLALCHEMY_ECHO = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://hm:hm@localhost:5432/hm"
    CANONICAL_NAME = '127.0.0.1'
    SSL_CERT_FILENAME = ''
    SSL_PRIVATE_KEY_FILENAME = ''
    TESTING = False
    USE_SSL = False
    # Flask-Cache settings
    # CACHE_TYPE = 'memcached'
    # CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']



#  If we're running in SSL mode, check for the files or give users a hint on
# how to generate the keys.
# if USE_SSL:
#     import os
#     key_file = SSL_PRIVATE_KEY_FILENAME if SSL_PRIVATE_KEY_FILENAME else 'ssl.key'
#     cert_file = SSL_CERT_FILENAME if SSL_CERT_FILENAME else 'ssl.cert'
#     if not os.access(key_file, os.R_OK) and not os.access(cert_file, os.R_OK):
#         print "HINT: To generate a key and cert without it prompting for information (spaces are escaped with a \\):\n"
#         print "\topenssl req -x509 -nodes -days 365 -subj '/C=US/ST=MyState/L=MyCity/CN=127.0.0.1/O=MyCompany\ Inc/OU=MyOU/emailAddress=user@example.com' -newkey rsa:1024 -keyout %s -out %s\n" % (key_file, cert_file)
#         raise ValueError('SSL_PRIVATE_KEY_FILENAME file missing (possibly needs to be generated?)')

#     else:
#         if not os.access(key_file, os.R_OK):
#             print "HINT: To generate a private key:\n"
#             print "\topenssl genrsa 1024 > %s\n" % key_file
#             raise ValueError('SSL_PRIVATE_KEY_FILENAME file missing (possibly needs to be generated?)')

#         if not os.access(cert_file, os.R_OK):
#             print "HINT: To generate a private key:\n"
#             print "\topenssl req -new -x509 -nodes -sha1 -days 365 -key %s > %s\n" % (key_file, cert_file)
#             raise ValueError('SSL_CERT_FILENAME file missing (possibly needs to be generated?)')

#     from OpenSSL import SSL
#     ctx = SSL.Context(SSL.TLSv1_METHOD)
#     ctx.use_privatekey_file(key_file)
#     ctx.use_certificate_file(cert_file)
#     WERKZEUG_OPTS['ssl_context'] = ctx

#     ### WARNING: Ugh. Monkey pach in a fix to correct pyOpenSSL's
#     ### incompatible ServerSocket implementation that accepts zero arguments
#     ### for shutdown() instead of one. Fix up
#     ### lib/python2.7/SocketServer.py:459's shutdown() call because that
#     ### appears to be easier to quickly hack in versus patching
#     ### pyOpenSSL. Again, don't use this for production, but it's great for
#     ### testing.
#     def monkeyp_ssl_shutdown_request(self, request):
#         try:
#             request.shutdown()
#         except socket.error:
#             pass #some platforms may raise ENOTCONN here
#         self.close_request(request)
#     from SocketServer import TCPServer
#     TCPServer.shutdown_request = monkeyp_ssl_shutdown_request

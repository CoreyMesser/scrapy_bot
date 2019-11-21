import os

class EnvConstants(object):
    TARGET_SITE = os.environ.get('TARGET_SITE')
    PATH_WATCHLIST = os.environ.get('PATH_WATCHLIST')
    TARGET_USER = os.environ.get('TARGET_USER')
import os

class EnvConstants(object):
    TARGET_SITE = os.environ.get('TARGET_SITE')
    PATH_WATCHLIST = os.environ.get('PATH_WATCHLIST')
    PATH_USER = os.environ.get('PATH_USER')
    TARGET_USER = os.environ.get('TARGET_USER')
    PATH_LOGIN = os.environ.get('PATH_LOGIN')
    TARGET_PW = os.environ.get('TARGET_PW')
    CF_DUID = os.environ.get('CF_DUID')
    G_CAPTCHA = os.environ.get('G_CAPTCHA')
    CF_B = os.environ.get('CF_B')
    CF_A = os.environ.get('CF_A')
    HEADERS = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0'
    ACC_DISABLED = os.environ.get('ACC_DISABLED')
    DATABASE = os.environ.get('DATABASE')


class AWSConstants(object):
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    BUCKET = os.environ.get('BUCKET')
    TWITTER = 'twitter/'
    FILENAME = 'artist_list'
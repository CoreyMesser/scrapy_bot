import time
from logger import LoggerService

from flask import Flask
from config import DevConfg
import redis

from run import Processors

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6739)
app.config.from_object(DevConfg)

# pros = Processors()
#
#
# @app.route('/')
# def home():
#     pass
#
#
# @app.route('/update_artist', methods=['GET'])
# def update_artist():
#     pros.add_update_artists()
#
#
# @app.route('/update_social', methods=['GET'])
# def update_social():
#     pros.social_update()
#
#
# @app.route('/send_s3', methods=['GET'])
# def send_to_s3():
#     pros.send_twitter_list_s3()


if __name__ == '__main__':
    app.run()

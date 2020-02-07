import logging

class Logger(object):
    def __init__(self):
        logging.basicConfig(filename='artlog.log', format='%(asctime)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('artlog.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self):
        log = self.logger
        return log

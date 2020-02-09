import logging


class LoggerService(object):

    def get_logger(self):
        logging.basicConfig(filename='artlog.log', format='%(asctime)s - %(message)s', level=logging.INFO)
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        if logger.handlers:
            logger.handlers = []
        fh = logging.FileHandler('artlog.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger


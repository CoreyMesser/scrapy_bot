from logger import LoggerService
import connexion

_log = LoggerService().get_logger()


def app_run():
    _log.info("___SCRAPY STARTING___")
    try:
        app = connexion.App(__name__, port=8080, specification_dir='api/')
        app.add_api('openapi.yaml', arguments={'title': 'Artist Scraper'})
        app.run()
        _log.info("___API SERVER STARTED___")

    except Exception as e:
        _log.error(f"[ERROR] Scrapy failed to start due to: {e}")


if __name__ == '__main__':
    app_run()

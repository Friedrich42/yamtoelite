import logging

from src import conf
from src import config
from src.main_ym2tch import main


def launch_app():
    db_session = config(conf.DB_PATH)
    logger = logging.getLogger('main')
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)-15s %(name)s - %(levelname)s - %(message)s')

    main(db_session, logger)


if __name__ == '__main__':
    launch_app()

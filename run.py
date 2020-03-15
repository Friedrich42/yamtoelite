import logging

from src import conf
from src import config
from src import functions as f
from src.main_ym2tch import main


def launch_app():
    db_session = config(conf.DB_PATH)
    logger = logging.getLogger('main')
    with f.in_dir("logs"):
        logging.basicConfig(filename=f'app-{f.get_time()}.log', filemode='a', format='%(asctime)-15s %(name)s'
                                                                                     ' - %(levelname)s - %(message)s')
    logger.setLevel("DEBUG")

    main(db_session, logger)


if __name__ == '__main__':
    launch_app()

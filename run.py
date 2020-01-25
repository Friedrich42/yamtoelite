from src import conf
from src import config
from src.main_ym2tch import main


def launch_app():
    db_session = config(conf.DB_PATH)

    main(db_session)


if __name__ == '__main__':
    launch_app()

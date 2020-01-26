import datetime
import os

from pathvalidate import sanitize_filename, sanitize_filepath
from contextlib import contextmanager


def get_time():
    """ returns time in needed format """
    return datetime.datetime.now().replace(microsecond=0).isoformat().replace(':', '-')  # return time in right format


def log_error(error):
    """ creates logs folder and logs all the errors """
    with in_dir("logs"):
        time = get_time()  # get current time
        with open(f'error-{time}.log', 'w') as log:
            log.write(str(error))  # write log to the .log file

    print(error)
    return error

    # exit(1)  # exit


@contextmanager
def in_dir(path: str):
    """
        function to do something in any directory

        example:
        with in_dir("foo/bar"):
            do_smth()

        is equivalent to
        os.chdir("foo/bar")
        do_smth()
        os.chdir(".."*2)
    """
    if path[-1] == "/":
        path = path[:-1]
    if path[0:2] == "./":
        path = path[2:]

    deepness = path.count("/")
    if not os.path.exists(path):
        os.makedirs(path)  # if path not exists, creates the folder
    os.chdir(path)
    yield
    os.chdir("../" * (deepness + 1))


def filter_filename(path: str):
    return sanitize_filename(path)[:255]


def filter_filepath(path: str):
    return sanitize_filepath(path)
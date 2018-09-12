import platform
import logzero
from app.autotestconfig import logPath as path
from . import config

class log :

    def __init__(self) :
        self.logfile = path + 'flask.log'
        logzero.logfile(self.logfile, maxBytes = 1e6, backupCount = 3)
        import logging
        formatter = logging.Formatter('%(asctime)-15s - [%(filename)s: %(lineno)s] -%(levelname)s: %(message)s');
        logzero.formatter(formatter)
        logzero.loglevel(logging.ERROR)
        self.logger = logzero.logger


if __name__ == '__main__':
    input("You can not run main!")



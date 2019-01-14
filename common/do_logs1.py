import logging
from logging.handlers import RotatingFileHandler
import time
from common import dir_config

fmt = " %(asctime)s  %(levelname)s %(filename)s %(funcName)s [ line:%(lineno)d ] %(message)s"
datefmt = '%a, %d %b %Y %H:%M:%S'

handler_1 = logging.StreamHandler()

curTime = time.strftime("%Y-%m-%d %H:%M", time.localtime())


handler_2 = RotatingFileHandler(dir_config.logs_dir+"/Api_Autotest_log_{0}.log".format(curTime), backupCount=10,
                                encoding='utf-8')

logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, handlers=[handler_1, handler_2])


logger = logging.getLogger('test')


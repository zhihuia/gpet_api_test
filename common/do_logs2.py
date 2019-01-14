import logging
import logging.handlers as HD
from common import dir_config
import time


class MyLogger:

    def __init__(self):
        # 实例化logging对象
        self.logger = logging.getLogger("api_autoTest")
        self.logger.setLevel(logging.INFO)
        # 日志内容输出格式设置
        fmt = '%(asctime)s  %(filename)s  %(funcName)s [line:%(lineno)d] %(levelname)s %(message)s'
        datefmt = '%a, %d %b %Y %H:%M:%S'
        format = logging.Formatter(fmt, datefmt)
        curTime = time.strftime("%Y-%m-%d %H%M", time.localtime())
        # 输出日志到文件中
        handle_1 = HD.TimedRotatingFileHandler(dir_config.logs_dir + "/Api_Autotest_log_{0}.log".format(curTime),
                                               backupCount=20, encoding="utf-8")
        handle_1.setFormatter(format)
        handle_1.setLevel(logging.INFO)
        self.logger.addHandler(handle_1)
        # 输出日志到控制台
        hs = logging.StreamHandler()
        hs.setFormatter(format)
        hs.setLevel(logging.INFO)
        self.logger.addHandler(hs)

    # 配置日志收集器 - 存在放哪个文件，
    # 定义各种日志级别的方法，方便在其它文件中调用
    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, msg):
        self.logger.exception(msg)

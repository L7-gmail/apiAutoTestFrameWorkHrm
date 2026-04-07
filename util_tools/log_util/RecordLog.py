import logging
import os
import time
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
import colorlog

from config import setting

log_path = setting.FILE_PATH['log']
if not os.path.exists(log_path):
    os.mkdir(log_path)

logfile_name = log_path + r"\test.{}.log".format(time.strftime("%Y%m%d %H%M%S"))


class RecordLog:

    def __init__(self):
        pass

    @classmethod
    def log_color(cls):
        log_color_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s %(asctime)s - %(levelname)s - [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s',
            log_colors=log_color_config)

        return formatter

    def output_logging(self):
        logger = logging.getLogger(__name__)
        stream_format = self.log_color()
        # 防止重复打印日志
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter(
                "%(asctime)s - %(levelname)s - [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            )
            # 把log日志信息输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(stream_format)
            logger.addHandler(sh)

            # 把log日志信息输出到指定的文件中
            fh = RotatingFileHandler(filename=logfile_name, mode='a', maxBytes=5242880, backupCount=7, encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            logger.addHandler(fh)

        return logger


logs = RecordLog().output_logging()

if __name__ == '__main__':
    logs.debug("debug日志")
    logs.info("info日志")
    logs.warning("warning日志")
    logs.error("error日志")
    logs.critical("critical日志")

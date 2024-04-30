import logging
import datetime
from logging.handlers import RotatingFileHandler
import os

log_level = "INFO"

LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "ERROR": logging.ERROR,
}


# TODO: 直接单例返回
class Logger:
    """
    logging日志
    TODO: 修改调用方式。。。重写，删除enable 参数

    """

    def __init__(self, log_level=log_level):
        self.logger = logging.getLogger()
        self.log_level = log_level
        self.init_logger()
        self.reset_logger()
        self.custom_logger()
    
    def init_logger(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
    

    def reset_logger(self):
        # 每次被调用后，清空已经存在handler
        self.logger.handlers.clear()

    def custom_logger(self):
        self.log_level = LOG_LEVEL_MAP.get(self.log_level, logging.INFO)
        self.logger.setLevel(self.log_level)
        self.backup_count = 5  # 最多存放日志的数量

        # 控制台输出格式
        console_handler = logging.StreamHandler()  # 定义console handler
        fmt = f"%(asctime)s-%(processName)s-%(filename)s:%(lineno)d:%(levelname)s %(message)s"
        formatter = logging.Formatter(fmt)  # 定义该handler格式

        # TODO: 确认不会引发其他问题 txueduo
        record = logging.LogRecord(
            name='my_logger',
            level=logging.NOTSET,
            pathname="",
            lineno=10,
            msg='This is a log message',
            args=None,
            exc_info=None
        )
        process_name = (formatter.format(record).split("-")[3]) # ['2024', '04', '30 13:07:59,004', 'MainProcess', ':10:NOTSET This is a log message']
        process_name = process_name if process_name == "MainProcess" else "SubProcess"
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        # 文件写入格式

        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        filename = os.path.join(self.log_dir, f"liveroom_{timestamp}_{process_name}.log")
        file_handler = RotatingFileHandler(
            filename=filename,
            backupCount=self.backup_count,
            maxBytes=1024*1024*512, # 暂时设置为512m
            delay=True,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.log_level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

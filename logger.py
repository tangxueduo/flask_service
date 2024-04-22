import logging
import datetime
from logging.handlers import TimedRotatingFileHandler
import os
import time

logging_handler = None
error_handle = None

#TODO: 直接单例返回 
class Logger:
    """
    logging日志
    TODO: 修改调用方式。。。重写，删除enable 参数

    """
    def __init__(self, header='', enable = True, log_level=logging.DEBUG):
        self.header = header
        self.logger = logging.getLogger(header)
        if enable:
            self.log_level = log_level
        else:
            self.log_level = logging.NOTSET
        self.logger.setLevel(self.log_level)
        if logging_handler is not None:
            self._logger.addHandler(logging_handler)
        
        self.backup_count = 5  # 最多存放日志的数量

        # 控制台输出格式
        console_handler = logging.StreamHandler()                  # 定义console handler
        formatter = logging.Formatter(f'%(asctime)s {self.header} %(lineno)d: %(levelname)s  %(message)s')  #定义该handler格式
        console_handler.setFormatter(formatter)
        console_handler.setLevel(self.log_level)
        # 文件写入格式
        self.log_dir = "logs"
        os.makedirs(self.log_dir,exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        file_handler = TimedRotatingFileHandler(filename=os.path.join(self.log_dir, f'liveroom_{timestamp}.log'), when='D',
                                                    interval=1, backupCount=self.backup_count, delay=True,
                                                    encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(self.log_level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        # 获取日志记录
    
    def get_logger(self):
        return self.logger

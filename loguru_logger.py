import logging
import os
import sys
from logging.config import dictConfig

from loguru import logger as loguru_logger

LOG_FORMAT = (
    "<level>{level: <8}</level> "
    "{process.name} | "  # 线程名
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - "
    "<blue>{process}</blue> "
    "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)
LOG_NAME = ["uvicorn", "uvicorn.access", "uvicorn.error", "flask"]


class InterceptHandler(logging.Handler):
    """https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging"""

    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except AttributeError:
            level = logging._levelToName[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class Logging:
    """自定义日志"""

    def __init__(self):
        self.log_path = "logs"
        os.makedirs(self.log_path, exist_ok=True)
        self._init_logger()
        self._reset_log_handler()
        self._custom_access_log()

    def _init_logger(self):
        """初始化loguru配置"""
        loguru_logger.remove()
        loguru_logger.add(
            os.path.join(self.log_path, "error.log.{time:YYYY-MM-DD}"),
            format=LOG_FORMAT,
            level=logging.ERROR,
            rotation="00:00",
            retention="1 week",
            backtrace=True,
            diagnose=True,
        )
        loguru_logger.add(
            os.path.join(self.log_path, "info.log.{time:YYYY-MM-DD}"),
            format=LOG_FORMAT,
            level=logging.INFO,
            rotation="00:00",
            retention="1 week",
        )
        loguru_logger.add(
            os.path.join(self.log_path, "debug.log.{time:YYYY-MM-DD}"),
            format=LOG_FORMAT,
            level=logging.DEBUG,
            rotation="00:00",
            retention="2 day",
        )
        loguru_logger.add(
            sys.stdout,
            format=LOG_FORMAT,
            level=logging.INFO,
            colorize=True,
        )
        self.logger = loguru_logger

    def _reset_log_handler(self):
        """重置logging handlers配置"""
        for log in LOG_NAME:
            logger = logging.getLogger(log)
            logger.handlers = [InterceptHandler()]

    def _custom_access_log(self):
        access_log = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "access": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": '%(levelprefix)s %(asctime)s :: %(client_addr)s - "%(request_line)s" %(status_code)s',
                    "use_colors": True,
                },
            },
            "handlers": {
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
                "access_file": {
                    "formatter": "access",
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": f"{self.log_path}/access.log",
                    "encoding": "utf8",
                    "when": "midnight",
                    "interval": 1,
                    "backupCount": 7,
                },
            },
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["access", "access_file"],
                    "level": "INFO",
                },
            },
        }
        dictConfig(access_log)

    def get_logger(self):
        return self.logger 

logger = Logging().get_logger()

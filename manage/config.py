import logging


class Config(object):
    def __init__(self):
        self._cfg = {
            "log": {
                "format": "PID %(process)d %(asctime)s %(levelname)-5s %(threadName)-10s [%(lineno)d]%(name)-15s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "filename": "",
                "level": logging.DEBUG
            },
        }

    def dev(self):
        """
        开发环境配置
        :return:
        """
        self._cfg["log"]["level"] = logging.DEBUG

    def stage(self):
        """
        测试环境配置
        :return:
        """
        self._cfg["log"]["level"] = logging.DEBUG

    def pro(self):
        """
        生产环境配置
        :return:
        """
        self._cfg["log"]["level"] = logging.ERROR

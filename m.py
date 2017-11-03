#!/usr/bin/env python
"""
项目预处理
"""
import os

from manage.const import ENV

try:
    import fire
except:
    os.system("pip install fire")

import logging

logger = logging.getLogger("manage")


class Manager(object):
    """项目管理"""

    def __init__(self, e=1):
        self._e = e

    def deps(self, he=3):
        """
        安装依赖库
        :return:
        """
        os.system("pip install -r requirements.txt")

    def gen_deps(self):
        """
        生成依赖库
        :return:
        """
        os.system("pipreqs --force .")

    def run(self, e=ENV.dev):
        """
        通过参数运行不同的线上环境，默认为dev
        dev: 0
        stage: 1
        prod: 2

        :param e:
        :return:
        """
        logger.info("running on {} env".format(e))

        if e == ENV.dev:
            os.system("python main.py")
        elif e == ENV.stage:
            pass
        elif e == ENV.dev:
            pass
        else:
            logger.info("参数不正确")

    def gen_cfg(self, e=ENV.dev):
        """
        生成各个环境的配置文件
        :return:
        """
        pass


if __name__ == '__main__':
    logging.basicConfig(
        format='PID %(process)d %(asctime)s %(levelname)-5s %(threadName)-10s [%(lineno)d]%(name)-15s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )
    fire.Fire(Manager, name="manage")

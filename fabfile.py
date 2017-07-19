# -*- coding: utf-8 -*-
from fabric.context_managers import cd
from fabric.decorators import roles
from fabric.operations import local, run
from fabric.state import env

from kervice.utils.sh_util import cmd

env.roledefs = {
    'local': ["barry@127.0.0.1"],
    'dev': ['centos@192.168.202.1'],
    'uat': ['centos@172.16.8.2'],
    "pro": [
        "centos@172.16.10.1:22",
        "centos@172.16.10.2:22",
    ]
}
env.passwords = {
    "centos@172.16.0.0:22": "123456",

}

env.colorize_errors = True
env.warn_only = True

env.pty = False
env.parallel = True


def local_init():
    """初始化本地依赖工具"""
    local("pip install pipreqs")
    local("pip install ujson")
    local("pip install click")
    local("pip install sanic")
    local("pip install Sanic-Cors")
    local("pip install AoikLiveReload")


def gen_reqs():
    """
    生成requirements
    :return:
    """
    cmd("pipreqs -f .")


def run_app(env="local", port="8100"):
    """
    运行本地项目
    fab run_app:"log='debug',env='dev',port=8100"
    fab run_app:log='debug',env='dev',port=8100
    """

    cmd("ps -ef | grep -v grep | grep kervice")
    _cmd = """python kervice -e {env} -p {port}""".format(env=env, port=port)
    local(_cmd)


def run_test(app_addr="http://localhost:8080", name=None):
    """
    fab run_test:"app_addr='http://localhost:8080',name='test'"
    :param app_addr:
    :param name:
    :return:
    """
    import os
    for i in os.listdir("t"):
        if not name:
            cmd("pyresttest {} t/{}.yaml".format(app_addr, i))
        else:
            cmd("pyresttest {} t/{}.yaml".format(app_addr, name))
            break


def _clone(p_name='kervice'):
    run("rm -rf /home/centos/projects/{}".format(p_name))
    with cd("/home/centos/projects"):
        run('git clone http://barry:12345678@192.168.200.19/math_model/{}.git --depth=1'.format(p_name))


def _restart(p_name='kervice'):
    run("curl -XPOST http://localhost:11313/api/programs/{}/stop".format(p_name))
    run("curl -XPOST http://localhost:11313/api/programs/{}/start".format(p_name))
    run("curl http://localhost:11313/api/programs/{}".format(p_name))


@roles("dev")
def dp_dev():
    _clone()
    _restart()


@roles("uat")
def dp_uat():
    _clone()
    _restart()


@roles("pro")
def dp_pro():
    _clone()
    _restart()

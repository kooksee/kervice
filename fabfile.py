# -*- coding: utf-8 -*-
from fabric.context_managers import cd
from fabric.decorators import roles
from fabric.operations import local, run
from fabric.state import env

env.roledefs = {
    'local': ["barry@127.0.0.1"],
    'dev': ['centos@192.168.202.215'],
    'uat': ['centos@172.16.8.125'],
    "pro": [
        "centos@172.16.10.144:22",
        "centos@172.16.10.145:22",
    ]
}
env.passwords = {
    'centos@172.16.8.125:22': "centosshanghai2015",
    'centos@192.168.202.215:22': "centosoffice2015",
    "centos@172.16.10.144:22": "centoswuxi2015",
    "centos@172.16.10.145:22": "centoswuxi2015",

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


def run_app(env="local", port="8100"):
    """
    运行本地项目
    fab run_app:"log='debug',env='dev',port=8100"
    fab run_app:log='debug',env='dev',port=8100
    """

    local(
        """
        python kervice -e {env} -p {port}
        """.format(env=env, port=port)
    )


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

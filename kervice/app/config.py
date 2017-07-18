from os.path import abspath as ap, dirname as dn

from kervice.app.const import Env
from kervice.utils import pp
from kervice.utils.app import Application


class Config(object):
    SECRET_KEY = '123456@#$%^&*('
    ROOT_PATH = dn(dn(dn(ap(__file__))))


class LocalConfig(Config):
    REDIS = {
        "address": ("127.0.0.1", 6379),
    }

    # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
    MONGODB_URI = "mongodb://localhost:27017"
    MONGODB_DB = "kservices"


class DevConfig(Config):
    REDIS = {
        "address": ("192.168.202.205", 9221),
        "password": None,
        "db": 0
    }


class UatConfig(Config):
    DEBUG = False
    REDIS = {
        "address": ("192.168.202.214", 9221),
        "password": None,
        "db": 0
    }


class ProConfig(Config):
    DEBUG = False
    REDIS = {
        "address": ("172.16.10.19", 9221),
        "password": None,
        "db": 0
    }


def init_config():
    app = Application.current()

    _e = app.env
    if _e == Env.local:
        _f = LocalConfig()
    elif _e == Env.dev:
        _f = DevConfig()
    elif _e == Env.uat:
        _f = UatConfig()
    elif _e == Env.production:
        _f = ProConfig()
    else:
        _f = LocalConfig()

    app.config.from_object(_f)


if __name__ == '__main__':
    print(pp(__file__, ap, dn, dn, dn))
    pass

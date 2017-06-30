# -*- coding: utf-8 -*-
class Config:
    NAME = "scores"
    DEBUG = True
    SECRET_KEY = '123456@#$%^&*('


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
    from utils.app import Application
    app = Application.current()

    from scores.const import Env

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

    app.config = _f
    app.debug = _f.DEBUG
    app.name = _f.NAME

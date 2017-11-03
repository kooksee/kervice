#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('proj', include=['proj.tasks'])

app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()

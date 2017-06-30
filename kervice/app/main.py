# -*- coding: utf-8 -*-
import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


import logging
import sys

from kervice.utils.app import Application
from kervice.utils.net_tool import get_host_ip

app = Application.current()

log = logging.getLogger(__name__)

async def __update_service():
    st, _res = await app.redis.execute("srem", "{}.url".format(app.name + ".zmq"), app.zmq_addr)
    if not st:
        print(_res)


def term_sig_handler(sig, stack_frame):
    log.info('catched singal: {},{}'.format(sig, stack_frame))
    asyncio.ensure_future(__update_service())
    sys.exit(0)

async def init_app():
    app = Application.current()

    from kervice.app.config import init_config
    init_config()
    from kervice.utils.redis_util import init_redis
    init_redis()

    app.url = "{}:{}".format(get_host_ip(), app.port)
    st, _ = await app.redis.execute("sadd", "{}.url".format(app.name), app.url)
    assert st != 0

    from signal import signal, SIGTERM, SIGINT, SIGQUIT
    signal(SIGTERM, term_sig_handler)
    signal(SIGINT, term_sig_handler)
    signal(SIGQUIT, term_sig_handler)

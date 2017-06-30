# -*- coding: utf-8 -*-
import asyncio

import uvloop

from utils.service_util import init_service

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def _main():
    from scores.handler import UrlHandler
    u = UrlHandler()
    while 1:
        try:
            await u.wacai_score()
        except Exception as e:
            print(e)


async def init_app():
    from utils.app import Application
    app = Application.current()

    from scores.config import init_config
    from utils.redis_util import init_redis
    from utils.log_util import log_callback
    from utils.log import KLog
    init_config()
    init_redis()
    KLog(callback=log_callback if not app.debug else None).init_log()

    await init_service()

    asyncio.run_coroutine_threadsafe(_main(), asyncio.get_event_loop())

    from kservices.config import init_config
    from kservices.handlers import init_handle
    from kservices.urls import init_url
    from utils.redis_util import init_redis

    init_handle()
    init_config()
    init_url()
    init_redis()

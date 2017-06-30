import time


class RedisManager(object):
    def __init__(self, config=None):
        self.config = config
        self.__r = None

    async def execute(self, command, *args, **kwargs):
        try:
            self.__r = self.__r or await self._conn()
            return 1, await getattr(self.__r, command)(*args, **kwargs)
        except Exception as e:
            if self.__r.closed:
                self.__r = None
            return 0, str(e)

    async def _conn(self):
        import aioredis
        _r = self.config
        address = _r.get("address")  # address:('localhost', 6379)
        password = _r.get("password")
        db = _r.get("db", 0)
        kwargs = _r.get("kwargs", {})
        return await aioredis.create_reconnecting_redis(address, password=password, db=db, encoding='utf-8', **kwargs)


def init_redis():
    from utils.app import Application
    app = Application.current()
    app.redis = RedisManager(config=app.config.REDIS)


async def _main():
    r = RedisManager(config={
        "address": ('localhost', 6379)
    })

    while 1:
        _st = time.time()
        await asyncio.sleep(1)
        # await r.execute('hmset_dict', 'ss', {"dd": 3})  # "dd", 2, "gg", 4

        # d = await r.execute('hmget', 'ss', "dd", "gg")
        st, d = await r.execute('hget', 'ss', 'dd')
        print(d)
        if not st:
            print(d)

        if d:
            pass

            # print(d)
            # print("time_used:", time.time() - _st)

            # d = await r.execute('info')
            # print(d)
            # d = await r.execute('info1')
            # print(d)


if __name__ == '__main__':
    import asyncio

    asyncio.run_coroutine_threadsafe(_main(), asyncio.get_event_loop())
    asyncio.get_event_loop().run_forever()

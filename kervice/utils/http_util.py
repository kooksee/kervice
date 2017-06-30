import aiohttp


async def __request_get(url, timeout=1, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            with aiohttp.Timeout(timeout):
                async with session.get(url, **kwargs) as response:
                    return 1, await response.text()
        except Exception as e:
            return 0, str(e)


async def request_get(url, timeout=1, num_retry=3, **kwargs):
    i = num_retry
    err_msg = []
    while i > 0:
        st, res = await __request_get(url, timeout=timeout, **kwargs)
        if not st:
            i -= 1
            err_msg.append(res)
            continue

        return 1, res
    else:
        return 0, err_msg


async def __request_post(url, data, timeout=1, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            with aiohttp.Timeout(timeout):
                async with session.post(url, data=data, **kwargs) as response:
                    return 1, await response.text()
        except Exception as e:
            return 0, str(e)


async def request_post(url, data, timeout=1, num_retry=3, **kwargs):
    i = num_retry
    err_msg = []
    while i > 0:
        st, res = await __request_post(url, data, timeout=timeout, **kwargs)
        if not st:
            i -= 1
            err_msg.append(res)
            continue

        return 1, res
    else:
        return 0, err_msg


async def main():
    st, ct = await request_get('http://www.baidu.com/')
    print(st)
    print(ct)


if __name__ == '__main__':
    import paco


    paco.run(main())

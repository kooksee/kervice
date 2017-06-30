import ujson as json

import paco

from kervice.utils.app import Application
from kervice.utils.http_util import request_post


def dingding_msg(data):
    cnt = data.get("cnt", "test: 我就是我, 是不一样的烟火")
    is_at_all = data.get("is_at_all", False)
    return {
        "msgtype": "text",
        "text": {
            "content": cnt
        },
        "at": {
            "isAtAll": is_at_all
        }}


async def _dingding_post(data):
    """
    data:{
        "msgtype": "text",
        "text": {
            "content": "我就是我, 是不一样的烟火"
        },
        "at": {
            "isAtAll": true
        }
    }

    :param data:
    :return:
    """
    url = "https://oapi.dingtalk.com/robot/send?access_token=8a42f363b58050141b1a13e24312d28ada51dfd00d4d2d231b934ac7557994fd"
    st, res = await request_post(url, json.dumps(data), headers={
        'content-type': "application/json",
        'cache-control': "no-cache"
    })
    if not st:
        print(data)
        print({"error": res})

def notice_add_handle(data):
    print(data)
    return "ok"


@paco.interval(0.2)
async def _notify_start_handle():
    app = Application.current()

    r = app.redis

    st, data = await r.execute("rpop", "notice")
    if not st:
        print(data)
        return

    if not data:
        return

    data = json.loads(data)
    msgtype = data.get("msgtype")
    if msgtype == 'notice':
        dingding_post(dingding_msg(data.get("notice")))
    elif msgtype == 'log':
        from bussiness.log import log_post
        log_post(data.get("log"))
    else:
        print(data)


async def notify_start_handle():
    app = Application.current()

    async def _f():
        f = await _notify_start_handle()
        print(f)

    app.timers["notice"] = run_async(_f())


def notify_stop_handle():
    app = Application.current()

    try:
        notice = app.timers["notice"]
        del app.timers["notice"]
        notice.cancel()
    except Exception as e:
        print(e)

from sanic.response import json


async def ok(req):
    print(req)
    return json({
        "status": "ok"
    })

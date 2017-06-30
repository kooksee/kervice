from utils import run_async


async def __log_post(data):
    """
    data:{
        "cnt": "内容: text",
        "name": "服务名字: text"
    }

    :param data:
    :return:
    """

    name = data.get("name", "test")
    cnt = data.get("cnt", {})

    from utils.app import Application
    app = Application.current()

    st, col = app.mongo.col(name)
    result = await col.insert_one(cnt)
    print('result %s' % repr(result.inserted_id))


def log_post(data):
    run_async(__log_post(data))

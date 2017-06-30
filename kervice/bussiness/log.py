from kervice.utils.app import Application


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

    app = Application.current()

    st, col = app.mongo.col(name)
    result = await col.insert_one(cnt)
    print('result %s' % repr(result.inserted_id))

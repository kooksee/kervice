import os
from asyncio import iscoroutine

from kervice.utils.colors import yellow, red


def when(func, arg1, arg2):
    """
    苦于python的三元表达式，远没有其他语言的方便，所以就自己创造了一个
    when(lambda x: x > 4, 'ok', 'no')(2)
    'no'
    when(3 > 4, 'ok', 'no')
    'no'
    when(lambda x: x > 4, lambda x:x*3, 'no')(6)(3)
    9
    when(lambda x: x > 4,when(lambda x: x > 6,'yes','no2'),'no1')(5)(1)
    'no2'
    :param func:
    :param arg1:
    :param arg2:
    :return:
    """
    if not callable(func):
        if func:
            return arg1
        else:
            return arg2
    else:
        def _t(*args, **argks):
            if func(*args, **argks):
                return arg1
            else:
                return arg2

        return _t


def pp(data, *func):
    if not data:
        print(yellow("data is {}".format(str(data))))

    async def __pp(data, *func):
        for f in func:
            if not iscoroutine(f):
                data = f(data)
            else:
                data = await f(data)

    return __pp(data, *func)


def init_pid_name(name):
    _pid = str(os.getpid())
    _pid_name = "{}.pid".format(_pid)

    _path = os.path.join(os.getenv("HOME"), ".services/{}".format(name))
    if not os.path.exists(_path):
        os.makedirs(_path)

    assert not os.path.exists(os.path.join(_path, _pid_name))
    with open(os.path.join(_path, _pid_name), 'w') as f:
        f.write(_pid)
    return name


def rm_pid_name(name):
    _path = os.path.join(os.getenv("HOME"), ".services/{}".format(name))
    _pid_path = os.path.join(_path, "{}.pid".format(str(os.getpid())))
    os.remove(_pid_path)
    if not os.path.exists(_pid_path):
        print(yellow("删除进程文件成功", _pid_path))
    else:
        print(red("删除进程文件失败", _pid_path))

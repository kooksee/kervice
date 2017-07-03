from kervice.utils.colors import yellow


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


class pp(object):
    def __init__(self, data):
        if not data:
            print(yellow("data is {}".format(str(data))))
        self._d = data

    def then(self, func):
        if not self._d:
            print(yellow("data is {}".format(str(self._d))))
        self._d = func(self._d)
        return self

    def result(self):
        return self._d


def h(x):
    print(x)
    return x


if __name__ == '__main__':
    pp("kk").then(h).then(h).then(print)
    pass

# -*- coding:utf-8 -*-



def get_host_user():
    """
    获得主机用户
    :return:
    """
    try:
        import getpass
        return getpass.getuser()
    except Exception as e:
        return None


def get_host_ip():
    """
    获得主机本地IP
    :return:
    """
    try:
        import socket
        return socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    except Exception as e:
        return 'localhost'


def get_host_name():
    """
    获得主机名
    :return:
    """
    try:
        import socket
        return socket.getfqdn(socket.gethostname())
    except Exception as e:
        return None


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == '__main__':
    print(get_open_port())
    pass




def init_url():
    from kervice.utils.app import Application
    app = Application.current()

    from kervice.app.handlers import ok
    app.route("/", methods=["GET"])(ok)

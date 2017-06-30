

def init_url():
    from kervice.utils.app import Application
    app = Application.current()
    app.route("/", methods=["GET"])(ok)

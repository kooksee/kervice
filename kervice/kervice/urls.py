def init_url():
    from utils.app import Application
    app = Application.current()

    from kservices.handlers import notice_add, notify_start, notify_stop, ok, services_get, services_post, \
        services_properties_get as spg
    app.route("/api/notice", methods=["POST"])(notice_add)
    app.route("/api/notify", methods=["POST"])(notify_start)
    app.route("/api/notify", methods=["DELETE"])(notify_stop)
    app.route("/api/services", methods=["POST"])(services_post)
    app.route("/api/services", methods=["GET"])(services_get)
    app.route("/api/service/property", methods=["GET"])(spg)
    app.route("/api/service/params", methods=["GET"])(spg)
    app.route("/service/status", methods=["GET"])(ok)
    app.route("/", methods=["GET"])(ok)

# -*- coding: utf-8 -*-

import threading

from sanic import Sanic


class Application(Sanic):
    # Global lock for creating global Application instance
    _instance_lock = threading.Lock()

    _current = threading.local()

    @staticmethod
    def instance():
        """Returns a global `Application` instance.

        Most applications have a single, global `Application` running on the
        main thread.  Use this method to get this instance from
        another thread.  In most other cases, it is better to use `current()`
        to get the current thread's `Application`.
        """
        if not hasattr(Application, "_instance"):
            with Application._instance_lock:
                if not hasattr(Application, "_instance"):
                    # New instance after double check
                    Application._instance = Application()
        return Application._instance

    @staticmethod
    def initialized():
        """Returns true if the singleton instance has been created."""
        return hasattr(Application, "_instance")

    def install(self):
        """Installs this `Application` object as the singleton instance.

        This is normally not necessary as `instance()` will create
        an `Application` on demand, but you may want to call `install` to use
        a custom subclass of `Application`.

        When using an `Application` subclass, `install` must be called prior
        to creating any objects that implicitly create their own
        `Application` (e.g., :class:`tornado.httpclient.AsyncHTTPClient`).
        """
        assert not Application.initialized()
        Application._instance = self

    @staticmethod
    def clear_instance():
        """Clear the global `Application` instance.

        .. versionadded:: 4.0
        """
        if hasattr(Application, "_instance"):
            del Application._instance

    @staticmethod
    def current(instance=True):
        """Returns the current thread's `Application`.

        If an `Application` is currently running or has been marked as
        current by `make_current`, returns that instance.  If there is
        no current `Application`, returns `Application.instance()` (i.e. the
        main thread's `Application`, creating one if necessary) if ``instance``
        is true.

        In general you should use `Application.current` as the default when
        constructing an asynchronous object, and use `Application.instance`
        when you mean to communicate to the main thread from a different
        one.

        .. versionchanged:: 4.1
           Added ``instance`` argument to control the fallback to
           `Application.instance()`.
        """
        current = getattr(Application._current, "instance", None)
        if current is None and instance:
            return Application.instance()
        return current

    def make_current(self):
        """Makes this the `Application` for the current thread.

        An `Application` automatically becomes current for its thread
        when it is started, but it is sometimes useful to call
        `make_current` explicitly before starting the `Application`,
        so that code run at startup time can find the right
        instance.

        .. versionchanged:: 4.1
           An `Application` created while there is no current `Application`
           will automatically become current.
        """
        Application._current.instance = self

    @staticmethod
    def clear_current():
        Application._current.instance = None

    @classmethod
    def configurable_base(cls):
        return Application

    def initialize(self, make_current=None):
        if make_current is None:
            if Application.current(instance=False) is None:
                self.make_current()
        elif make_current:
            if Application.current(instance=False) is not None:
                raise RuntimeError("current Application already exists")
            self.make_current()

# -*- coding:utf-8 -*-

from threading import local


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        super(Singleton, cls).__init__(*args, **kwargs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance


class SlothBaseException(Exception):
    """
        Provide a base exception object for Sloth
    """

    pass


class ThreadSafeObject(local):
    """
        Provide a thread safe base object for Sloth.
    """

    pass


class SlothRouter(object):
    """
        Provide a base router class for Sloth.
    """

    def __init__(self, response, *args, **kwargs):
        self.response = response

        self.initialize()

    @property
    def status(self):
        return self.response.status

    @property
    def headers(self):
        return self.response.headers

    def initialize(self):
        """ Initial Something
            Call for each router
        """

        pass

    def execute(self):
        return self.response.start_response()

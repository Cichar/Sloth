# -*- coding:utf-8 -*-

from threading import local


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

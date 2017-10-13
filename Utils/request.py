# -*- coding:utf-8 -*-

from .baseobject import ThreadSafeObject


class SlothRequest(ThreadSafeObject):
    def __init__(self):
        self.__environ = None

    def bind_environ(self, environ):
        self.__environ = environ

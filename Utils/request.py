# -*- coding:utf-8 -*-

from .baseobject import ThreadSafeObject


class SlothRequest(ThreadSafeObject):
    def __init__(self, environ):
        self.__environ = environ

    @property
    def path(self):
        return self.__environ.get('PATH_INFO', None)

    @property
    def method(self):
        return self.__environ.get('REQUEST_METHOD', 'GET')

    @property
    def query_string(self):
        return self.__environ.get('QUERY_STRING', '')

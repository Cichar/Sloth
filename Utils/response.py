# -*- coding:utf-8 -*-

from .baseobject import ThreadSafeObject


class SlothResponse(ThreadSafeObject):
    def __init__(self):
        self.__status = '200 '
        self.__headers = [('Content-type', 'text/plain')]

        self.__body = None

    def set_body(self, body):
        self.__body = body().encode()

    def set_status(self, status: int):
        self.__status = '%s ' % status

    @property
    def status(self):
        return self.__status

    @property
    def headers(self):
        return self.__headers

    @property
    def body(self):
        return self.__body

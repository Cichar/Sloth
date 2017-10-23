# -*- coding:utf-8 -*-

from http import HTTPStatus

normal_response = {v: v.phrase for v in HTTPStatus.__members__.values()}


class Router(object):
    """ Object for register router
        Example:
            class IndexHandler(SlothResponse):
                def get(self, *args, **kwargs):
                    self.render_string('Hello World!')

            routers = [Router(path='/hello', response=IndexHandler)]
    """

    def __init__(self, path: str, response: object, name: str=None):
        if not isinstance(path, str) or isinstance(name, str):
            raise TypeError('Path must be string type, get %s' % type(path))
        self.path = path
        self.response = response
        self.name = name

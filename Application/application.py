# -*- coding:utf-8 -*-

from Utils.exception import HandlerException


class Application(object):
    def __init__(self, handlers: dict=None):
        if handlers:
            self._handlers = handlers
        else:
            raise HandlerException('Application Need At Least One Handler. '
                                   'But Application.handlers = %s' % handlers)

    def __call__(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b"Hello world\n"]

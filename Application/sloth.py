# -*- coding:utf-8 -*-

from Utils.exception import HandlerException


class Sloth(object):
    """
        This is the Application class for Sloth.

        Example:
            from Sloth.Server import Server
            from Sloth.Application import Sloth

            urls = {'/': handler}
            app = Sloth(handlers=urls)
            server = Server(app)

            server.start() # default run on http://127.0.0.1:8555

    """

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

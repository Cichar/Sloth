# -*- coding:utf-8 -*-

from Utils.router import RouterManager
from Utils.request import SlothRequest
from Utils.response import SlothResponse
from Utils.exception import HandlerException


class Sloth(object):
    """
        This is the Application class for Sloth.

        Example:
            from Sloth.Server import Server
            from Sloth.Application import Sloth

            urls = {'/': router}
            app = Sloth(routers=urls)
            server = Server(app)

            server.start() # default run on http://127.0.0.1:8555

    """

    __server__ = 'Sloth Server'
    __version__ = 1.0

    def __init__(self, routers: dict=None):
        if not routers:
            raise HandlerException('Application Need At Least One Router. '
                                   'But Sloth.routers = %s' % routers)
        self._response_cls = SlothResponse
        self._router_manager = RouterManager(self, routers, self._response_cls)

    def _handler_request(self, request):
        response = self._router_manager.get_response(request)
        return response

    def __call__(self, environ, start_response):
        request = SlothRequest(environ)
        response = self._handler_request(request)
        result = response.execute()
        start_response(response.status, response.headers)
        return result

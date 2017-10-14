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

    def __init__(self, routers: dict=None):
        if routers:
            self._routers = routers
        else:
            raise HandlerException('Application Need At Least One Router. '
                                   'But Sloth.routers = %s' % routers)

        self._response_cls = SlothResponse
        self._router_manager = RouterManager(routers, self._response_cls)

    def _handler_request(self):
        try:
            response = self._router_manager.get_response(self._request.path, self._request.method)
            return response
        except Exception:
            pass

    def __call__(self, environ, start_response):
        self._request = SlothRequest(environ)
        response = self._handler_request()

        start_response(response.status, response.headers)
        return [response.body]

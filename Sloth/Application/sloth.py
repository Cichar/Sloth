# -*- coding:utf-8 -*-

from Sloth.Utils.exception import HandlerException
from Sloth.Utils.response import SlothResponse
from Sloth.Utils.router import RouterManager
from Sloth.Utils.request import SlothRequest


class Sloth(object):
    """
        This is the Application class for Sloth.

        Example:
            from Sloth.Server import Server
            from Sloth.Application import Sloth
            from Sloth.Utils.response import SlothResponse

            class IndexHandler(SlothResponse):
                def get(self, num, name=None):
                    self.render_string('Hello %s! This is num %s' % (name, num))

            routers = [Router(path='/hello/<name>/(\d+)', response=IndexHandler)]
            app = Sloth(routers=routers)
            server = Server(app)

            server.start() # default run on http://127.0.0.1:8555

    """

    __server__ = 'Sloth Server'
    __version__ = 1.0

    def __init__(self, routers: list=None):
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
        status, headers, result = response.execute()
        start_response(status, headers)
        return result

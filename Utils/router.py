# -*- coding:utf-8 -*-

from Utils.baseobject import Singleton


class RouterManager(object, metaclass=Singleton):
    """ Manager for Sloth's routers/handlers.
        This class must only be an instance object in Sloth class.
    """

    def __init__(self, routers, response_cls):
        self._not_stored_routers = routers
        self._routers = {}
        self._response_cls = response_cls

    def register_routers(self):
        pass

    @staticmethod
    def _http_error_404():
        return 'The Page Was Not Found'

    def get_response(self, path, method):
        response = self._response_cls()
        router = self._routers.get(path, None)

        # if router is exist, then return correct response
        # else assert the router is not exist, return default 404 response
        if router:
            response.set_body(router)
        else:
            response.set_status(404)
            response.set_body(self._http_error_404)
        return response

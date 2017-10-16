# -*- coding:utf-8 -*-

from Utils.baseobject import Singleton
from Utils.exception import RouterException
from Utils.exception import RegisterException
from Utils.exception import RouterTypeException


class Router(object):
    """ Rule for register router in Sloth """

    def __init__(self, path: str, router, name=None):
        self.name = name
        self.path = self.parse_path(path)
        self.router = router

    @staticmethod
    def parse_path(path):
        return '.'

    def execute(self):
        self.router.start_response()


class RouterManager(object, metaclass=Singleton):
    """ Manager for Sloth's routers/handlers.
        This class must only be an instance object in Sloth class.
    """

    def __init__(self, app: object, routers: dict, response_cls):
        self.application = app
        self._response_cls = response_cls
        self.__registered = False
        self._routers = self.register_routers(routers)

    def register_routers(self, routers: dict):
        """ Register routers.
            This function will return a router dict.
            Example:
                pass
        """

        registered_routers = {}

        for path, _router in routers.items():
            if not callable(_router):
                raise RouterException('Router must be a callable function.')
            if not issubclass(_router, self._response_cls):
                raise RouterTypeException('Router must be the subclass of %s.' % self._response_cls.__name__)
            router = Router(path, _router)
            registered_routers[path] = router

        self.__registered = True
        return registered_routers

    def find_router(self, request):
        """ Parse request PATH_INFO.
            then find the router which in or not in this manager
        """

        router = self._routers.get(request.path, None)
        return router

    def get_router(self, request):
        """ Use request to get the router, which registered in this manager.
            If registered flag is not True, maybe register func not execute.
            then raise RegisterException()
        """

        if not self.__registered:
            raise RegisterException('RouterManager has no routers map, '
                                    'maybe register function not execute.')
        router = self.find_router(request)
        return router

    def get_response(self, request):
        router = self.get_router(request)

        # if router is exist, then return correct response
        # else assert the router is not exist, return default 404 response
        if router:
            response = router(self.application)
            response.receive_request(request)
        else:
            response = self._response_cls(self.application)
            response.set_status(404)
        return response

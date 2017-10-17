# -*- coding:utf-8 -*-

from Utils.baseobject import Singleton
from Utils.baseobject import SlothRouter
from Utils.exception import RouterException
from Utils.exception import RegisterException
from Utils.exception import RouterTypeException


class _Router(SlothRouter):
    """ Rule for register router in Sloth """

    def __init__(self, path: str, response, name=None, *args, **kwargs):
        self.name = name
        self.path = self.parse_path(path)
        super().__init__(response, *args, **kwargs)

    @staticmethod
    def parse_path(path):
        """ This function will verify soon """
        return ''

    def __repr__(self):
        return str({'name': self.name, 'path': self.path})


class _HTTPErrorRouter(SlothRouter):
    def __init__(self, response, status_code, *args, **kwargs):
        self.status_code = status_code
        super().__init__(response, *args, **kwargs)

    def initialize(self):
        self.response.set_status(self.status_code)


class RouterManager(object, metaclass=Singleton):
    """ Manager for Sloth's routers/handlers.
        This class must only be an instance object in Sloth class.
    """

    def __init__(self, app: object, routers: dict, response_cls):
        self.application = app
        self._response_cls = response_cls
        self.__registered = False

        self._routers = self.register_routers(routers)
        self.routers = self._routers

    def register_routers(self, routers: dict):
        """ Register routers.
            This function will return a router dict.
            Example:
                pass
        """

        registered_routers = {}

        for path, response in routers.items():
            if not callable(response):
                raise RouterException('Response must be a callable function.')
            if not issubclass(response, self._response_cls):
                raise RouterTypeException('Response must be the subclass of %s.' % self._response_cls.__name__)
            router = _Router(path, response)
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
            response = _HTTPErrorRouter(self._response_cls(self.application), 404)
        return response

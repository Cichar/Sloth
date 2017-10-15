# -*- coding:utf-8 -*-

from Utils.baseobject import Singleton


class RouterRule(object):
    """ Rule for register router in Sloth """

    def __init__(self, path, router):
        self.path = path
        self.router = router

    def execute(self):
        self.router.start_response()


class RouterStore(object):
    """ Register the routers """

    def __init__(self, routers):
        self.__unregistered_routers = routers
        self.__registered_routers = self.register_routers()

    def register_routers(self):
        """ Register routers in Store. 
        """

        registered_routers = {}

        for path, router in self.__unregistered_routers:
            pass

        return registered_routers

    def find_router(self, request):
        return self.__registered_routers.get(request.path, None)


class RouterManager(object, metaclass=Singleton):
    """ Manager for Sloth's routers/handlers.
        This class must only be an instance object in Sloth class.
    """

    def __init__(self, app, routers, response_cls):
        self._routers = self.register_routers(routers)
        self._response_cls = response_cls
        self.application = app

    @staticmethod
    def register_routers(routers):
        return RouterStore(routers)

    def get_router(self, request):
        router = self._routers.find_router(request)
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

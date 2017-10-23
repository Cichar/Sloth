# -*- coding:utf-8 -*-

import re

from .baseobject import Singleton
from .baseobject import SlothRouter
from .exception import RouterException
from .exception import RegisterException
from .exception import RouterTypeException
from .exception import RouterArgTypeException


class _PathMatch(object):
    """ Path Match Rule For Router """

    _int = '\d+'
    _string = '\w+'
    _re_group = re.compile("<.+>")

    def __init__(self, path):
        if isinstance(path, str):
            _regex = self.construct(path)
            if not _regex.endswith('$'):
                _regex += '$'
            self.regex = re.compile(_regex)

    def construct(self, path):
        """ Construct formatted url path.
            Example:
                '/hello/<name>'  -->  '/hello/(?P<name>.+)'
                '/hello/<name:int>'  -->  '/hello/(?P<name>\d+)'
                '/hello/<name:string>'  -->  '/hello/(?P<name>\w+)'
        """

        groups = path.split('/')

        for k, v in enumerate(groups):
            v = v.replace(' ', '')
            if self._re_group.match(v):
                _ = v[1:-1].split(':')
                if len(_) > 1:
                    _type = getattr(self, '_' + _[1], None)
                    if _type:
                        groups[k] = '(?P<%s>%s)' % (_[0], getattr(self, '_' + _[1]))
                    else:
                        raise RouterArgTypeException("type %s is not support. if you don't know "
                                                     "which type you need choose, you can set <name>. the "
                                                     "other is <name:int>、<name:string>" % _[1])
                else:
                    groups[k] = '(?P' + v + '.+' + ')'

        _path = '/'.join(groups)

        return _path

    def match(self, path):
        """ Match path
            if exist, then return args and kwargs
            Example:
                Router('/hello/(\d+)')
                Request.PATH_INFO = '/hello/123'
                return {router_args: [123], router_kwargs: {}}

                Router('/hello/<name>')
                Request.PATH_INFO = '/hello/name123'
                return {router_args: [], router_kwargs: {'name': 'name123'}}

                Router('/hello/<name>/(\d+)')
                Request.PATH_INFO = '/hello/sloth/123'
                return {router_args: [123], router_kwargs: {'name': 'sloth'}}
        """

        match = self.regex.match(path)

        # if request.path is not match
        # assert the router is not exist return None
        if not match:
            return None

        # if regex has no groups
        # assert the router don't need args and kwargs
        if not self.regex.groups:
            return {}

        router_args, router_kwargs = [], {}

        # if groupindex is exist, assert the path has named arg.
        if self.regex.groupindex:
            router_kwargs = dict((str(k), v) for (k, v) in match.groupdict().items())
        router_args = [arg for arg in match.groups() if arg not in router_kwargs.values()]

        return dict(router_args=router_args, router_kwargs=router_kwargs)


class _Router(SlothRouter):
    """ Rule for register router in Sloth """

    def __init__(self, path: str, response, name=None, *args, **kwargs):
        self.name = name
        self.path = path
        self.matcher = _PathMatch(path)
        super().__init__(response, *args, **kwargs)

    def __repr__(self):
        return str("Router(path='{0}', response={1}, name='{2}')".format(
                    self.path, self.response.__class__, self.name))


class _HTTPErrorRouter(SlothRouter):
    def __init__(self, request, response, status_code, *args, **kwargs):
        self.request = request
        self.status_code = status_code
        super().__init__(response, *args, **kwargs)

    def initialize(self):
        self.response.set_status(self.status_code)
        self.response.receive_request(self.request)


class RouterManager(object, metaclass=Singleton):
    """ Manager for Sloth's routers/handlers.
        This class must only be an instance object in Sloth class.
    """

    def __init__(self, app: object, routers, response_cls):
        self.application = app
        self._response_cls = response_cls
        self.__registered = False

        self._routers = self.register_routers(routers)

    @property
    def routers(self):
        return self._routers

    def register_routers(self, routers):
        """ Register routers.
            This function will return a router list.
            Example:
                [
                    Router(path='/', response=<class '__main__.IndexHandler'>, name='index')
                    Router(path='/hello', response=<class '__main__.HelloHandler'>, name='hello')
                ]
        """

        registered_routers = []

        for router in routers:
            if not callable(router.response):
                raise RouterException('Response must be a callable function.')
            if not issubclass(router.response, self._response_cls):
                raise RouterTypeException('Response must be the subclass of %s.' % self._response_cls.__name__)
            _router = _Router(router.path, router.response(self.application), name=router.name)
            registered_routers.append(_router)

        self.__registered = True
        return registered_routers

    def find_router(self, request):
        """ Use request to find the router, which registered in this manager.
            If registered flag is not True, maybe register func not execute.
            then raise RegisterException(); else parse request PATH_INFO.
            then find the router which in or not in this manager
        """

        if not self.__registered:
            raise RegisterException('RouterManager has no routers map, '
                                    'maybe register function not execute.')

        # if router is exist, then return correct response
        # else assert the router is not exist, return default 404 response
        for router in self._routers:
            match = router.matcher.match(request.path)
            if match is not None:
                router.response.receive_request(request)
            else:
                router = _HTTPErrorRouter(request, self._response_cls(self.application), 404)
            return router

    def get_response(self, request):
        router = self.find_router(request)
        return router

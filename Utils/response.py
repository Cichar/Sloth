# -*- coding:utf-8 -*-

from .objects import normal_response
from .baseobject import ThreadSafeObject
from .exception import HTTPError
from .exception import ResponseException


class SlothResponse(ThreadSafeObject):
    SUPPORT_METHODS = ['HEAD', 'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

    def __init__(self, app):
        self.application = app
        self._request = None
        self._prepare = False
        self._finished = False
        self.__status_code = None
        self.__reason = None
        self.__headers = []
        self.__body = []

        self.clear()
        self.initialize()

    @property
    def status(self):
        return '%s ' % self.__status_code

    @property
    def headers(self):
        return self.__headers

    @property
    def body(self):
        return self.__body

    def receive_request(self, request):
        self._request = request

    def clear(self):
        """ Reset all headers and content.
        """

        self.__headers = [('Server', 'SlothServer/%s' % self.application.__version__)]
        self.__status_code = 200
        self.__reason = normal_response[200]

    def head(self, *args, **kwargs):
        """ If Router Method Support ''HEAD'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def get(self, *args, **kwargs):
        """ If Router Method Support ''GET'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def post(self, *args, **kwargs):
        """ If Router Method Support ''POST'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def put(self, *args, **kwargs):
        """ If Router Method Support ''PUT'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def delete(self, *args, **kwargs):
        """ If Router Method Support ''DELETE'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def options(self, *args, **kwargs):
        """ If Router Method Support ''OPTIONS'',
            Subclass need to implement this method,
        """

        raise HTTPError(405)

    def initialize(self):
        """ Initial Something
            Called for each response.
            If need, Subclass need to implement this method.
            Execute:
                Initialize --> Prepare --> finish --> on_finish
        """
        pass

    def prepare(self):
        """ Prepare Something
            Called for each response. 
            If need, Subclass need to implement this method.
            Execute:
                Initialize --> Prepare --> finish --> on_finish
        """
        pass

    def finish(self, chunk):
        """ Finish The Request, Before on_finish()
            Called for each response. 
            Execute:
                Initialize --> Prepare --> finish --> on_finish
        """

        if self._finished:
            raise RuntimeError("finish() called twice.")

        self.__body.append(self.to_bytes(chunk))
        self._finished = True
        self.on_finish()

    def on_finish(self):
        """ After finish()
            Called for each response. 
            If need, Subclass need to implement this method.
            Execute:
                Initialize --> Prepare --> finish --> on_finish
        """
        pass

    def set_status(self, status_code: int, reason=None):
        """ Set status for response 
        """

        self.__status_code = status_code
        if reason:
            self.__reason = reason
        else:
            try:
                self.__reason = normal_response[status_code]
            except KeyError:
                raise ValueError("Unknown HTTP Error Code %d" % status_code)
        self.finish(self.__reason)

    @staticmethod
    def to_bytes(chunk):
        """ If chunk object is not bytes,
            Conversion chunk to bytes then return,
            else return immediately.
        """

        if not isinstance(chunk, bytes):
            return bytes(chunk, 'utf-8')
        else:
            return chunk

    def render_template(self, *args, **kwargs):
        """ This function will verify soon """
        self.finish(*args, **kwargs)

    def start_response(self):
        """ Start to handler request.
            :return: response body
        """

        try:
            if self._request.method not in self.SUPPORT_METHODS:
                raise HTTPError(405)
            if not self._prepare:
                self.prepare()

            getattr(self, self._request.method.lower())()
        except Exception as err:
            self._handler_request_exception(err)
        else:
            return self.body

    def _handler_request_exception(self, err):
        raise err

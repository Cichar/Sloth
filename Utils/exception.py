# -*- coding:utf-8 -*-

from .objects import normal_response
from .baseobject import SlothBaseException


class HandlerException(SlothBaseException):
    pass


class RouterException(SlothBaseException):
    pass


class RouterTypeException(SlothBaseException):
    pass


class RegisterException(SlothBaseException):
    pass


class ResponseException(SlothBaseException):
    pass


class HTTPError(SlothBaseException):
    def __init__(self, status_code: int, message: str = None, *args, **kwargs):
        self.status_code = status_code
        self.message = message
        self.reason = kwargs.get('reason', None)

    def __str__(self):
        message = "HTTP %d: %s" % (self.status_code,
                                   self.reason or normal_response[self.status_code])
        if self.message:
            return message + "(" + self.message + ")"
        else:
            return message

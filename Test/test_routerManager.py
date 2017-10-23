# -*- coding:utf-8 -*-

from Sloth.Application import Sloth
from Sloth.Utils.objects import Router
from Sloth.Utils.router import RouterManager
from Sloth.Utils.response import SlothResponse


class IndexHandler(SlothResponse):
    pass


if __name__ == '__main__':
    routers = [Router(path='/', response=IndexHandler)]
    manager = RouterManager(Sloth, routers, SlothResponse)
    print(manager.routers)

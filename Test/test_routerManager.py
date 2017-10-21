# -*- coding:utf-8 -*-

from Sloth.Utils.router import RouterManager

from Sloth.Utils.response import SlothResponse


class IndexHandler(SlothResponse):
    pass


if __name__ == '__main__':
    manager = RouterManager(None, {'test_handler': IndexHandler}, SlothResponse)
    manager.register_routers({'test_handler': IndexHandler})
    print(manager.routers)

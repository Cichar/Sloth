# -*- coding:utf-8 -*-

from Sloth.Application import Sloth
from Sloth.Utils.response import SlothResponse

from Sloth.Server import Server


class IndexHandler(SlothResponse):
    pass


app = Sloth(routers={'/': IndexHandler})
server = Server(app)

if __name__ == '__main__':
    server.start()

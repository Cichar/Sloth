# -*- coding:utf-8 -*-

from Server import Server
from Application import Sloth
from Utils.response import SlothResponse


class IndexHandler(SlothResponse):
    pass


app = Sloth(routers={'/': IndexHandler})
server = Server(app)

if __name__ == '__main__':
    server.start()

# -*- coding:utf-8 -*-

from Sloth.Application import Sloth
from Sloth.Utils.objects import Router
from Sloth.Utils.response import SlothResponse

from Sloth.Server import Server


class IndexHandler(SlothResponse):
    def get(self, num, name=None):
        self.render_string('Hello %s! This is num %s' % (name, num))


routers = [Router(path='/hello/<name>/(\d+)', response=IndexHandler)]
app = Sloth(routers=routers)
server = Server(app)

if __name__ == '__main__':
    server.start()

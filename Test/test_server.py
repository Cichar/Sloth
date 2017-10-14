# -*- coding:utf-8 -*-

from Server import Server
from Application import Sloth

app = Sloth(routers={'test_handler': 'test'})
server = Server(app)

if __name__ == '__main__':
    server.start()

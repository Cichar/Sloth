# -*- coding:utf-8 -*-


from Server.server import Server
from Application.application import Application

if __name__ == '__main__':
    Server(Application).start()

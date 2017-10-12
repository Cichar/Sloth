# -*- coding:utf-8 -*-


class Server(object):
    def __init__(self, host: str='127.0.0.1', port: int=8888):
        self.host = host
        self.port = port

    def start(self):
        pass

    def __repr__(self):
        return '{0} ({1}:{2})'.format(self.__class__.__name__, self.host, self.port)

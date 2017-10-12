# -*- coding:utf-8 -*-


class Server(object):
    def __init__(self, app, host: str='127.0.0.1', port: int=8555):
        self._host = host
        self._port = port
        self.application = app

    def start(self):
        from wsgiref.simple_server import make_server

        try:
            server = make_server(self._host, self._port, self.application)
            print('Sloth on http://{0}:{1}'.format(self._host, self._port))
            server.serve_forever()
        except KeyboardInterrupt:
            pass

    def __repr__(self):
        return '{0} ({1}:{2})'.format(self.__class__.__name__, self._host, self._port)

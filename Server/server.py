# -*- coding:utf-8 -*-


class Server(object):
    def __init__(self, app: object, host: str='127.0.0.1', port: int=8555):
        self._host = host
        self._port = port
        self.application = app

    def start(self):
        try:
            server = self._make_server()
            print('Sloth run on http://{0}:{1}'.format(self._host, self._port))
            server.serve_forever()
        except KeyboardInterrupt:
            # server.shutdown()
            pass

    def _make_server(self):
        from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

        server = WSGIServer((self._host, self._port), WSGIRequestHandler)
        server.set_app(self.application)
        return server

    def __repr__(self):
        return '{0} ({1}:{2})'.format(self.__class__.__name__, self._host, self._port)

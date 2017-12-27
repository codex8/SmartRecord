# -*- encoding:utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from minicap import Stream
from queue import Queue
import threading

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        q = Queue()
        a = Stream.getBuilder(ip='127.0.0.1', port=1313, queue=q)
        a.run()
        print('open')
        self.tag = True

        def skt():
            while self.tag:
                self.write_message(q.get(), binary=True)

        self.t = threading.Thread(target=skt)
        self.t.start()
        pass

    def on_message(self, message):
        self.write_message(u"Your message was: " + message)

    def on_close(self):
        self.tag = True
        print('close')
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
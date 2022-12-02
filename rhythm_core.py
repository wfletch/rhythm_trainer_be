import zmq
from zmq.asyncio import Context
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
import tornado
ctx = zmq.Context.instance()
s = ctx.socket(zmq.REP)
s.bind("tcp://127.0.0.1:5555")

stream = zmq.eventloop.zmqstream.ZMQStream(s)


def echo(msg):
    print(msg)
    stream.send_multipart(msg)


stream.on_recv(echo)
tornado.ioloop.IOLoop.instance().start()
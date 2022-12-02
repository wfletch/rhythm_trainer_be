import zmq
from zmq.asyncio import Context
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
import tornado
import asyncio
import datetime
ctx = zmq.Context.instance()
MIDI_socket = ctx.socket(zmq.REP)
MIDI_socket.bind("tcp://127.0.0.1:5555")

MIDI_input_stream = zmq.eventloop.zmqstream.ZMQStream(MIDI_socket)

second_delay = 5
def echo(msg):
    MIDI_input_stream.send_multipart(msg, copy=True)
    if len(msg) == 1:
        # We have a control message
        msg = msg[0].decode('utf-8')
        print(msg)
        if msg == 1:
            # Do Action One
            print("TEMPO UP")
            second_delay -=1
        if msg == 2:
            # Do Action One
            print("TEMPO DOWN")
            second_delay+=1
        if msg == 3:
            # Do Action One
            print("PAUSE")
            second_delay += 10000000000
        if msg == 4:
            # Do Action One
            print("RESET")
   


def wrapper():
    print ("TEST")
    next_tick = datetime.datetime.now().timestamp() + second_delay 
    tornado.ioloop.IOLoop.current().add_timeout(next_tick, wrapper)

MIDI_input_stream.on_recv(echo, copy=True)
wrapper()
tornado.ioloop.IOLoop.instance().start()
import zmq
from zmq.asyncio import Context
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
import tornado
import asyncio
import datetime

d_hash = {"second_delay" : 5, "enabled" : True}
ctx = zmq.Context.instance()
MIDI_socket = ctx.socket(zmq.REP)
MIDI_socket.bind("tcp://127.0.0.1:5555")

MIDI_input_stream = zmq.eventloop.zmqstream.ZMQStream(MIDI_socket)
system_snapshot = {}
def echo(msg):
    ack_msg = "ACK"
    if len(msg) == 1:
        # We have a control message
        msg = msg[0].decode('utf-8')
        if msg == "TEMPO_UP":
            # Do Action One
            print("TEMPO UP")
            d_hash["second_delay"] -=1
        if msg == "TEMPO_DOWN":
            # Do Action One
            print("TEMPO DOWN")
            d_hash["second_delay"] +=1
        if msg == "TEMPO_PAUSE":
            # Do Action One
            print("PAUSE")
            d_hash["enabled"] = not d_hash["enabled"] 
            if d_hash["enabled"]:
                next_tick = datetime.datetime.now().timestamp() + d_hash["second_delay"]
                tornado.ioloop.IOLoop.current().add_timeout(next_tick, wrapper)
        if msg == "TEMPO_RESET":
            # Do Action One
            print("RESET")
        if msg == "GET_SNAPSHOT":
            ack_msg = system_snapshot
        MIDI_input_stream.send_string(ack_msg, copy=True)
            
   


def wrapper():
    print ("TEST: ")
    next_tick = datetime.datetime.now().timestamp() + d_hash["second_delay"]
    print(d_hash)
    if d_hash["enabled"]:
        tornado.ioloop.IOLoop.current().add_timeout(next_tick, wrapper)

MIDI_input_stream.on_recv(echo, copy=True)
wrapper()
tornado.ioloop.IOLoop.instance().start()
import zmq
from zmq.asyncio import Context
from zmq.eventloop.zmqstream import ZMQStream
from zmq.eventloop import ioloop
import tornado
import asyncio
import datetime
import json

current_bpm = 60
current_beat_count = 1
current_max_beats = 4
d_hash = {
    "second_delay": 60 / 240,
    "enabled": True,
    "current_bpm": current_bpm,
    "current_beat_count": current_beat_count,
    "current_max_beats": current_max_beats,
}
ctx = zmq.Context.instance()
MIDI_socket = ctx.socket(zmq.REP)
MIDI_socket.bind("tcp://127.0.0.1:5555")

MIDI_input_stream = zmq.eventloop.zmqstream.ZMQStream(MIDI_socket)
system_snapshot = {}


def echo(msg):
    ack_msg = "ACK"
    if len(msg) == 1:
        # We have a control message
        msg = msg[0].decode("utf-8")
        if msg == "TEMPO_UP":
            # Do Action One
            print("TEMPO UP")
            d_hash["current_bpm"] += 10
            d_hash["second_delay"] = 60 / (d_hash["current_bpm"] * d_hash["current_max_beats"])
        if msg == "TEMPO_DOWN":
            # Do Action One
            print("TEMPO DOWN")
            d_hash["current_bpm"] -= 10
            d_hash["second_delay"] = 60 / (d_hash["current_bpm"] * d_hash["current_max_beats"])
        if msg == "TEMPO_PAUSE":
            # Do Action One
            print("PAUSE")
            d_hash["enabled"] = not d_hash["enabled"]
            if d_hash["enabled"]:
                next_tick = datetime.datetime.now().timestamp() + d_hash["second_delay"]
                tornado.ioloop.IOLoop.current().add_timeout(next_tick, metronome_tick)
        if msg == "TEMPO_RESET":
            # Do Action One
            print("RESET")
        # Convert to hash
        print("HERE WE ARE!!!")
        print(msg)
        try:
            msg = json.loads(msg)
            print(msg)
            if msg["message"] == "GET_SNAPSHOT":
                print("SNAPSHOT REQUEST")
                ack_msg = {
                    "id": msg["id"],
                    "current_beat": d_hash["current_beat_count"] % d_hash["current_max_beats"],
                    "bpm": d_hash["current_bpm"],
                }
                print(ack_msg)
                MIDI_input_stream.send_string(json.dumps(ack_msg)) 
            else:
                MIDI_input_stream.send_string(ack_msg, copy=True)
        except Exception as e:
            MIDI_input_stream.send_string(ack_msg, copy=True) 
            print("oops? \n" , e)


def metronome_tick():
    d_hash["current_beat_count"] +=1
    next_tick = datetime.datetime.now().timestamp() + d_hash["second_delay"]
    print(d_hash)
    if d_hash["enabled"]:
        tornado.ioloop.IOLoop.current().add_timeout(next_tick, metronome_tick)


MIDI_input_stream.on_recv(echo, copy=True)
metronome_tick()
tornado.ioloop.IOLoop.instance().start()

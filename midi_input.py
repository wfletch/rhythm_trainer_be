import mido
import time
import signal
import sys
import logging
import zmq
def signal_handler(signal, frame):
    print("You pressed Ctrl+C - or killed me with -2")
    # TODO: Close Midi
    sys.exit(0)
message_mapping = { '1': "TEMPO_UP",
                    '2': "TEMPO_DOWN",
                    '3': "TEMPO_PAUSE",
                    '4': "TEMPO_RESET"
                    }
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

signal.signal(signal.SIGINT, signal_handler)
names = mido.get_input_names()
print(names)
inport = mido.open_input()
# Blocks Messages
while True:
    msg = inport.receive()
    print(msg.control)
    socket.send_string(message_mapping[str(msg.control)])
    message = socket.recv()
    # We should Send a request message change.
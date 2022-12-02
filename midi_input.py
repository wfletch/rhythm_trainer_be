import mido
import time
import signal
import sys

def signal_handler(signal, frame):
    print("You pressed Ctrl+C - or killed me with -2")
    # TODO: Close Midi
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
names = mido.get_input_names()
print(names)
inport = mido.open_input()

# Blocks Messages
while True:
    msg = inport.receive()
    print(msg)
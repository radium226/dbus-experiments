#!/usr/bin/env python

from gi.repository import GLib

from dbus.bus import BusConnection
from dbus.mainloop.glib import DBusGMainLoop
from dbus.service import BusName, Object, method, signal

from threading import Thread
from pathlib import Path

from os import getenv

from collections import namedtuple

from functools import partial

from subprocess import Popen, PIPE

from time import sleep


DBUS_ADDRESS = "tcp:host=broker,port=12345"

BUS_NAME = "com.github.radium226.Experiment"
OBJECT_PATH = "/Streamer"
DBUS_INTERFACE = "com.github.radium226.experiment.Streamer"


Size = namedtuple("Size", ["width", "height"])

def ffplay_command(size):
    return [
        "ffplay",
        "-autoexit",
        "-v", "quiet",
        "-f", "rawvideo",
        "-pixel_format",
        "bgr24",
        "-video_size", f"{size.width}x{size.height}",
        "-i", "-"
    ]

def handle_frame(process_stdin, frame_bytes):
    process_stdin.write(bytes(frame_bytes))

def main():
    size = Size(800, 600)

    mainloop = GLib.MainLoop()
    DBusGMainLoop(set_as_default=True)

    sleep(10)

    bus = BusConnection(getenv("DBUS_ADDRESS") or DBUS_ADDRESS)
    remote_object = bus.get_object(BUS_NAME, OBJECT_PATH)

    process = Popen(ffplay_command(size), stdin=PIPE)
    remote_object.connect_to_signal("FrameEmitted", partial(handle_frame, process.stdin), dbus_interface=DBUS_INTERFACE)
    remote_object.EmitFrames()

    #print(remote_object.Capitalize("hello world"))
    
    print("Starting player... ", flush=True)
    mainloop.run()
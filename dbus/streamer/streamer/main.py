#!/usr/bin/env python

from gi.repository import GLib

from dbus.bus import BusConnection
from dbus.mainloop.glib import DBusGMainLoop
from dbus.service import BusName, Object, method, signal

from threading import Thread
from pathlib import Path

from os import getenv

from subprocess import Popen, PIPE

from collections import namedtuple

from time import sleep


DBUS_ADDRESS = 'tcp:host=broker,port=12345'

BUS_NAME = 'com.github.radium226.Experiment'
OBJECT_PATH = '/Streamer'
DBUS_INTERFACE = 'com.github.radium226.experiment.Streamer'


Size = namedtuple("Size", ["width", "height"])

def ffmpeg_command(file_path, size):
    return [
        "ffmpeg",
        "-v", "quiet",
        "-i", str(file_path),
        "-f", "image2pipe",
        "-s", f"{size.width}x{size.height}",
        "-pix_fmt", "bgr24",
        "-vcodec", "rawvideo",
        "-"
    ]


class StreamerObject(Object):

    def __init__(self, bus, bus_name, file_path, size):
        super().__init__(bus, OBJECT_PATH, bus_name)
        self.file_path = file_path
        self.size = size

    @signal(DBUS_INTERFACE, signature="ay")
    def FrameEmitted(self, frame_bytes):
        pass

    @method(DBUS_INTERFACE, in_signature="", out_signature="")
    def EmitFrames(self):
        def thread_target():
            process = Popen(ffmpeg_command(self.file_path, self.size), stdout=PIPE)
            for frame_bytes in iter(lambda: process.stdout.read(3 * self.size.width * self.size.height), b""):
                self.FrameEmitted(frame_bytes)

        thread = Thread(target=thread_target)
        thread.start()

    @method(DBUS_INTERFACE, in_signature="s", out_signature="s")
    def Capitalize(self, text):
        return text.capitalize()


def main():
    file_path = Path("./ocean3.mp4")
    size = Size(800, 600)
    
    print("Starting streamer... ", flush=True)

    mainloop = GLib.MainLoop()
    DBusGMainLoop(set_as_default=True)

    bus = BusConnection(getenv("DBUS_ADDRESS") or DBUS_ADDRESS)
    bus_name = BusName(BUS_NAME, bus)

    StreamerObject(bus, bus_name, file_path, size)

    mainloop.run()
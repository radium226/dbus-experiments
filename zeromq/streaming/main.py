#!/usr/bin/env python

import click
import click_pathlib

from subprocess import Popen, PIPE
import zmq

from .size import Size, SIZE


@click.group()
def streaming():
    pass

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

@streaming.command()
@click.argument("file_path", type=click_pathlib.Path())
@click.argument("size", type=SIZE)
def stream(file_path, size):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://0.0.0.0:5557")
    process = Popen(ffmpeg_command(file_path, size), stdout=PIPE)
    print("Stream! ", flush=True)
    for frame_bytes in iter(lambda: process.stdout.read(3 * size.width * size.height), b""):
        zmq_socket.send(frame_bytes)
    zmq_socket.send(bytes([]))

@streaming.command()
@click.option("--zmq-socket-address", default="tcp://127.0.0.1:5557")
@click.argument("size", type=SIZE)
def play(zmq_socket_address, size):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PULL)
    zmq_socket.connect(zmq_socket_address)
    
    process = Popen(ffplay_command(size), stdin=PIPE)
    process_stdin = process.stdin
    print(f"Play {zmq_socket_address}! ", flush=True)
    while True:
        frame_bytes = zmq_socket.recv()
        if len(frame_bytes) == 0:
            process.kill()
            break
        process_stdin.write(frame_bytes)
        
    
def main():
    streaming()
#!/usr/bin/env python

import click
from click import INT
import click_pathlib

from subprocess import Popen, PIPE
from redis import Redis

from .size import Size, SIZE

STREAM_NAME = "video"


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
@click.option("--redis-host", default="127.0.0.1")
@click.option("--redis-port", default=6379, type=INT)
@click.argument("file_path", type=click_pathlib.Path())
@click.argument("size", type=SIZE)
def stream(redis_host, redis_port, file_path, size):
    redis = Redis(host=redis_host, port=redis_port)
    print("Stream! ", flush=True)
    process = Popen(ffmpeg_command(file_path, size), stdout=PIPE)
    for offset, frame_bytes in enumerate(iter(lambda: process.stdout.read(3 * size.width * size.height), b"")):
        print("Emit")
        redis.xadd(STREAM_NAME, {
            "bytes": frame_bytes
        })
    

@streaming.command()
@click.option("--redis-host", default="127.0.0.1")
@click.option("--redis-port", default=6379, type=INT)
@click.argument("size", type=SIZE)
def play(redis_host, redis_port, size):
    redis = Redis(host=redis_host, port=redis_port)
    process = Popen(ffplay_command(size), stdin=PIPE)
    process_stdin = process.stdin
    id = "0-0"
    while True:
        xread = redis.xread({
            STREAM_NAME: id, 
        }, count = 1)
        for stream, messages in xread:
            for id, fields in messages:
                frame_bytes = fields["bytes".encode("utf-8")]
                process_stdin.write(frame_bytes)
        
    
def main():
    streaming()
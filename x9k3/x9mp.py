#!/usr/bin/env python3

"""
x9k3/x9mp.py

cli tool for ABR
"""

import os
import sys
from m3ufu import M3uFu
from threefive import reader, blue
from .abr import ABR
from .x9k3 import argue, version
from .x9k3 import cli as x9cli


def do(args):
    """
    do runs x9k3.ABR programmatically.

    """
    fu = M3uFu()
    if not args.input:
        print("input source required (Set args.input)")
        sys.exit()
    fu.m3u8 = args.input
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    fu.decode()
    abr = ABR(fu.segments)
    abr.go()


def not_master(m3u8):
    """
    not_master returns True if
    m3u8 is not a master.m3u8
    """
    if m3u8 == sys.stdin.buffer:
        return True
    if m3u8.startswith(("srt://", "udp://")):
        return True


def is_master(m3u8):
    """
    is_master master.m3u8 detection
    """
    if not_master(m3u8):
        return False
    return b"#EXT-X-STREAM-INF" in reader(m3u8).read(1316)


def cli():
    """
    cli provides one function call
    to handle x9k3 with ABR support

    from x9k3.x9mp import cli
     cli()

    """
    args = argue()
    if args.version:
        print(version())
        sys.exit()
    _ = {blue(f"{k} = {v}") for k, v in vars(args).items()}
    if is_master(args.input):
        do(args)
    else:
        x9cli()


if __name__ == "__main__":
    cli()

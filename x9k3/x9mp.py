#!/usr/bin/env python3

import os
import sys
from .abr import ABR
from m3ufu import M3uFu
from threefive import reader
from .x9k3 import X9K3, argue, version
from .x9k3 import cli as x9cli


def do(args):
    """
    do runs umzz programmatically.
    Use like this:

    from umzz import do, argue

    args =argue()

    args.input = "/home/a/slow/master.m3u8"
    args.live = True
    args.replay = True
    args.sidecar_file="sidecar.txt"
    args.output_dir = "out-stuff"

    do(args)

    set any command line options
    programmatically with args.
    Here are the defaults returned from argue() .

    input='master.m3u8',
    continue_m3u8=False,
    delete=False,
    live=False,
    no_discontinuity=False,
    output_dir='.',
    program_date_time=False,
    replay=False,
    sidecar_file=None,
    shulga=False,
    time=2,
    hls_tag='x_cue',
    window_size=5,

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


def ismaster(m3u8):
    """
    ismaster master.m3u8 detection
    """
    return b"#EXT-X-STREAM-INF" in reader(m3u8).read()


def cli():
    """
    cli provides one function call
    for running shari with command line args
    Two lines of code gives you a full umzz command line tool.

     from umzz import cli
     cli()

    """
    args = argue()
    if args.version:
        print(version())
        sys.exit()
    _ = {print(k, "=", v) for k, v in vars(args).items()}
    if ismaster(args.input):
        do(args)
    else:
        x9cli()


if __name__ == "__main__":
    cli()

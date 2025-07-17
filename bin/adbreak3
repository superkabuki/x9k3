#!/usr/bin/env python3

"""
adbreak3

generates SCTE-35 cues for sidecar files
"""

import argparse
import os
from threefive import Cue, SpliceInsert


def argue():
    """
    argue parse command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=60.0,
        help="Set duration of ad break. [ default: 60.0 ]",
    )
    parser.add_argument(
        "-e",
        "--event-id",
        type=int,
        default=1,
        help="Set event id for ad break. [ default: 1 ]",
    )
    parser.add_argument(
        "-i",
        "--cue-in-only",
        action="store_const",
        default=False,
        const=True,
        help="Only make a cue-in SCTE-35 cue [ default: False ]",
    )
    parser.add_argument(
        "-o",
        "--cue-out-only",
        action="store_const",
        default=False,
        const=True,
        help="Only make a cue-out SCTE-35 cue [ default: False ]",
    )
    parser.add_argument(
        "-p",
        "--pts",
        type=float,
        default=0.0,
        help="Set start pts for ad break. Not setting pts will generate a Splice Immediate CUE-OUT. [ default: 0.0 ]",
    )
    parser.add_argument(
        "-P",
        "--preroll",
        action="store_const",
        default=False,
        const=True,
        help=" Add SCTE data four seconds before splice point. Used with MPEGTS. [ default: False ]",
    )
    parser.add_argument(
        "-s",
        "--sidecar",
        default="sidecar.txt",
        help="""Sidecar file of SCTE-35 (pts,cue) pairs. [ default: sidecar.txt ] """,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_const",
        default=False,
        const=True,
        help="Show version",
    )

    return parser.parse_args()


def mk_splice_insert(event_id, pts=None, duration=None, out=False):
    """
    mk_splice_insert returns a Cue with a Splice Insert.

    The args set the SpliceInsert vars.

    splice_event_id = event_id

    if pts is None (default):
        splice_immediate_flag      True
        time_specified_flag        False

    if pts:
        splice_immediate_flag      False
        time_specified_flag        True
        pts_time                   pts

    If duration is None (default)
        duration_flag              False

    if duration IS set:
        out_of_network_indicator   True
        duration_flag              True
        break_auto_return          True
        break_duration             duration
        pts_time                   pts

    if out is True:
        out_of_network_indicator   True

    if out is False (default):
        out_of_network_indicator   False

    """
    cue = Cue()
    # default is a CUE-IN
    sin = SpliceInsert()
    sin.splice_event_id = event_id
    sin.splice_event_cancel_indicator = False
    sin.out_of_network_indicator = out
    sin.duration_flag = False
    sin.unique_program_id = event_id
    sin.avail_num = 0
    sin.avails_expected = 0
    sin.splice_immediate_flag = True
    sin.time_specified_flag = False
    sin.program_splice_flag = True
    sin.event_id_compliance_flag = True
    # pts = None for Splice Immediate
    if pts:
        sin.splice_immediate_flag = False
        sin.time_specified_flag = True
        sin.pts_time = float(pts)
    else:
        sin.component_count = 0
    # If we have a duration, set duration
    if duration:
        duration = float(duration)
        sin.break_duration = duration
        sin.break_auto_return = True
        sin.duration_flag = True
        sin.out_of_network_indicator = True
    # Add SpliceInsert to the SCTE35 cue
    cue.command = sin
    cue.encode()
    return cue


def show_cue(new_cue):
    """
    show_cue displays cue data
    """
    cue = Cue(new_cue)
    cue.decode()
    head = "\t\tCUE-OUT"
    body = f"   PTS:{cue.command.pts_time}   Id:{cue.command.splice_event_id}"
    tail = f"   Duration: {cue.command.break_duration}"
    if not cue.command.out_of_network_indicator:
        head = f"\t\tCUE-IN "
        tail = "\n"
    print(head + body + tail)


# cue.command.show()


def cue_out(event_id, pts, duration, sidecar, preroll):
    """
    cue_out generates a SCTE-35 cue with out of network set to True
    """
    if args.pts == 0.0:
        cue = mk_splice_insert(event_id, duration=duration, out=True).encode()
    else:
        cue = mk_splice_insert(event_id, pts=pts, duration=duration, out=True).encode()
    write_line(pts - preroll, cue, sidecar)


def cue_in(event_id, pts, sidecar, preroll):
    """
    cue_in generates a SCTE-35 cue with out of network set to False
    """
    cue = mk_splice_insert(event_id, pts=pts, out=False).encode()
    write_line(pts - preroll, cue, sidecar)


def write_line(pts, cue, sidecar):
    """
    write_line writes pts,cue to sidecar file
    """
    show_cue(cue)
    line = f"{pts},{cue}\n"
    sidecar.write(line)


def mk_cues(args):
    """
    mk_cues generates cues for the sidecar
    based on the values in args
    """
    preroll = 0
    if args.preroll:
        preroll = 4
    event_id = args.event_id
    duration = args.duration
    pts = args.pts
    #   if pts == 0.0:
    #      args.cue_out_only = True
    print(f"\nWriting to sidecar file: {args.sidecar}\n")
    with open(args.sidecar, "a") as sidecar:
        if not args.cue_in_only:
            cue_out(event_id, pts, duration, sidecar, preroll)
            pts = pts + duration
            event_id += 1
        if not args.cue_out_only:
            cue_in(event_id, pts, sidecar, preroll)


if __name__ == "__main__":
    args = argue()
    mk_cues(args)

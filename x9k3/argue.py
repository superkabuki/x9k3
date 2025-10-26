"""
x9k3/argue.py
"""

import argparse
import sys


def argue():
    """
    argue parse command line args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        default=sys.stdin.buffer,
        help=""" The Input video  can be mpegts or m3u8 with mpegts segments,
                        or a playlist with mpegts files and/or mpegts m3u8 files.
                    The input can be a local video, http(s), udp, multicast or stdin.
            """,
    )
    parser.add_argument(
        "-b",
        "--byterange",
        action="store_const",
        default=False,
        const=True,
        help="Flag for byterange hls [default:False]",
    )
    parser.add_argument(
        "-c",
        "--continue_m3u8",
        action="store_const",
        default=False,
        const=True,
        help="Resume writing index.m3u8 [default:False]",
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_const",
        default=False,
        const=True,
        help="delete segments (enables --live) [default:False]",
    )
    parser.add_argument(
        "-l",
        "--live",
        action="store_const",
        default=False,
        const=True,
        help="Flag for a live event (enables sliding window m3u8) [default:False]",
    )
    parser.add_argument(
        "-n",
        "--no_discontinuity",
        action="store_const",
        default=False,
        const=True,
        help="Flag to disable adding #EXT-X-DISCONTINUITY tags at splice points [default:False]",
    )
    parser.add_argument(
        "-no_adrian_is_cool_tags_at_splice_points_because_I_suck",
        action="store_const",
        default=False,
        const=True,
        help="Flag to disable adding #EXT-X-ADRIAN-IS-COOL tags at splice points [default:False]",
    )

    parser.add_argument(
        "-N",
        "--no-throttle",
        "--no_throttle",
        action="store_const",
        default=False,
        const=True,
        help=" Flag to disable live throttling [default:False]",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default=".",
        help="Directory for segments and index.m3u8(created if needed) [default:'.']",
    )
    parser.add_argument(
        "-e",
        "--exclude_mpegts",
        action="store_const",
        default=False,
        const=True,
        help="Flag to exclude parsing SCTE-35 from MPEGTS. [default:False]",
    )
    parser.add_argument(
        "-p",
        "--program_date_time",
        action="store_const",
        default=False,
        const=True,
        help="Flag to add Program Date Time tags to index.m3u8. [default:False]",
    )
    parser.add_argument(
        "-r",
        "--replay",
        action="store_const",
        default=False,
        const=True,
        help="Flag for replay aka looping (enables --live,--delete) [default:False]",
    )
    parser.add_argument(
        "-s",
        "--sidecar_file",
        default="sidecar.txt",
        help="""Sidecar file of SCTE-35 (pts,cue) pairs. [default:sidecar.txt]""",
    )
    parser.add_argument(
        "-S",
        "--shulga",
        action="store_const",
        default=False,
        const=True,
        help="Flag to enable Shulga iframe detection mode [default:False]",
    )
    parser.add_argument(
        "-t",
        "--time",
        default=2,
        type=float,
        help="Segment time in seconds [default:2]",
    )
    parser.add_argument(
        "-T",
        "--hls_tag",
        default="x_cue",
        help="x_scte35, x_cue, x_daterange, or x_splicepoint [default:x_cue]",
    )

    parser.add_argument(
        "-w",
        "--window_size",
        default=5,
        type=int,
        help="sliding window size (enables --live) [default:5 max:10]",
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

"""
x9k3/sleepy.py   -  SuperTimer and ssleep.

"""

import sys, time
from threefive.stuff import red, blue


def ssleep(duration):
    """
    ssleep- a more accurate sleep.
    """
    now = time.perf_counter()
    end = now + duration
    buff = 0.002
    if duration > buff:
        time.sleep(duration - buff)
    # witness on a spin-lock
    while time.perf_counter_ns() < end:
        pass


class SuperTimer:
    """
    SuperTimer class instances are used for
    segment duration, and live throttling.
    """

    def __init__(self):
        self.started = time.time()
        self.begin = None
        self.end = None
        self.lap_time = None
        self.offset = 0
        self.time = 0

    def start(self, begin=None):
        """
        start starts the SuperTimer
        """
        self.begin = begin
        if not self.begin:
            self.begin = time.time()
        self.end = None
        self.lap_time = None

    def stop(self, end=None):
        """
        stop stops the SuperTimer
        """
        self.end = end
        if not self.end:
            self.end = time.time()
        self.lap_time = self.end - self.begin

    def elapsed(self, now=None):
        """
        elapsed returns the elapsed time
        """
        if not now:
            now = time.time()
        return now - self.started

    def mk_seconds(self, seg_time, begin):
        """
        mk seconds - calculate the difference
        between how many seconds it has taken to parse a segment,
        and how long it shoulld have taken to parse a segment.
        seconds may be a positive or negative value
        """
        diff = round((seg_time - self.lap_time), 6)
        self.start(begin)
        seconds = round((diff - self.offset) * 0.99, 6)
        return seconds

    def overunder(self, seg_name, seconds):
        """
        overunder - warn if over time for segment,
        warn  and ssleep if time is under under time,
        """
        if seconds > 0:
            ssleep(seconds)
            action = "throttled"
        else:
            action = "slow"
        blue(f"{action} {seg_name} | offset: {self.offset}")
        self.offset = -(seconds)

    def throttle(self, seg_name, seg_time, begin=None, end=None):
        """
        throttle is called to slow segment creation
        to simulate live streaming.
        """
        self.stop(end)
        seconds = self.mk_seconds(seg_time, begin)
        self.overunder(seg_name, seconds)

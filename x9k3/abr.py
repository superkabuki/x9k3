"""
abr.py
"""

from pathlib import Path
import os
import sys
import time
import multiprocessing as mp
from threefive import reader
from .x9k3 import X9K3, argue


class ABR:
    """
    The ABR class starts a X9MP process for each rendition
    and manages them.
    """

    def __init__(self, m3u8_list):
        #       mp.set_start_method("spawn")
        self.master = None
        self.m3u8_list = m3u8_list
        self.args = argue()
        self.sidecar = self.args.sidecar_file
        self.side_files = []
        self.last_stat = 0
        self.procs = []

    def add_rendition(self, m3u8, dir_name, rendition_sidecar=None):
        """
        add_rendition starts a process for each rendition and
        creates a pipe for each rendition to receive SCTE-35.
        """
        p = mp.Process(
            target=mp_run,
            args=(m3u8, dir_name, rendition_sidecar),
        )
        p.start()
        print(f"Rendition Process Started {dir_name}")
        self.procs.append(p)

    def load_sidecar(self):
        """
        load_sidecar reads (pts, cue) pairs from
        the sidecar file and loads them into X9K3.sidecar
        if live, blank out the sidecar file after cues are loaded.
        """
        with reader(self.sidecar) as sidefile:
            these_lines = sidefile.readlines()
            for side_file in self.side_files:
                print(f"Updating {side_file}")
                with open(side_file, "wb") as side:
                    side.writelines(these_lines)

    def _mk_rendition_sidecar(self, dir_name):
        rendition_sidecar = None
        if self.args.sidecar_file:
            _, tail = os.path.split(self.sidecar)
            rendition_sidecar = dir_name + "/" + tail
            Path(rendition_sidecar).touch()
            self.side_files.append(rendition_sidecar)
        return rendition_sidecar

    def _chk_master_sidecar(self):
        if self.sidecar:
            side_stat = os.stat(self.sidecar).st_mtime
            if side_stat != self.last_stat:
                self.load_sidecar()
                self.last_stat = side_stat

    def go(self):
        """
        go writes the new master.m3u8.
        """
        dir_name = 0
        with open(
            self.args.output_dir + "/master.m3u8", "w", encoding="utf-8"
        ) as master:
            master.write("#EXTM3U\n#EXT-X-VERSION:6\n\n")
            for m3u8 in self.m3u8_list:
                if "#EXT-X-STREAM-INF" in m3u8.tags:
                    master.write("\n".join(m3u8.lines[:-1]))
                    master.write("\n")
                    dn = self.args.output_dir + "/" + str(dir_name)
                    if not os.path.isdir(dn):
                        os.mkdir(dn)
                    master.write(f"{dir_name}/index.m3u8\n")
                    rendition_sidecar = self._mk_rendition_sidecar(dn)
                    self.add_rendition(m3u8, dn, rendition_sidecar)
                    dir_name += 1
                else:  # Copy over stuff like "#EXT-X-MEDIA-TYPE"
                    if len(m3u8.lines) > 1:
                        master.write("\n".join(m3u8.lines[:-1]))
                        media_uri = m3u8.lines[-1]
                        master.write(f"{media_uri}\n")
                        master.write("\n")
                    else:
                        master.write(m3u8.lines[0])
                        master.write("\n")
        while True in [p.is_alive() for p in self.procs]:
            self._chk_master_sidecar()
            time.sleep(0.2)
        sys.exit()


def mk_x9mp(manifest, dir_name, rendition_sidecar):
    """
    mk_x9mp generates an X9MP instance and
    sets default values
    """
    x9mp = X9K3()
    x9mp.args = argue()
    x9mp.args.output_dir = dir_name
    x9mp.args.input = manifest.media
    x9mp.args.sidecar_file = rendition_sidecar
    return x9mp


def mp_run(manifest, dir_name, rendition_sidecar=None):
    """
    mp_run is the process started for each rendition.
    """
    args = argue()
    x9mp = mk_x9mp(manifest, dir_name, rendition_sidecar)
    x9mp.decode()
    while args.replay:
        x9mp = mk_x9mp(manifest, dir_name, rendition_sidecar)
        x9mp.args.continue_m3u8 = True
        x9mp.continue_m3u8()
        x9mp.decode()
    return False

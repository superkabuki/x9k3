### How to Make Super Accurate SCTE-35 for ABR HLS with threefive ffmpeg. and x9k3.   
---
<BR>

#### 1. use threefive to generate a sidecar file from an MPEGTS stream.

```py3
#!/usr/bin/env python3

import sys
from threefive import Stream, Cue

def mk_sidecar_keyframes(cue):
    """
    mk_sidecar generates a sidecar file with the SCTE-35 Cues
    and a keyframes.txt files with iframe times for the SCTE-35
    """
    pts = 0.0
    with open("sidecar.txt", "a") as sidecar:
        with open('keyframes.txt','a') as keyframes:
            cue.show()
            if cue.packet_data.pts:
                pts = cue.packet_data.pts
                keyframes.write(f'{pts}\n')
            data = f'{pts},{cue.encode()}\n'
            sidecar.write(data)

if __name__ == '__main__':

    strm =Stream(sys.argv[1])
    strm.decode(func=mk_sidecar_keyframes)
```

* threefive will write two files sidecar.txt and keyframes.txt
---


#### 2. Use ffmpeg to encode ABR HLS from your mpegts stream.

* I don't want to debate HLS formating and such, encode it how you want but add  `-force-keyframes keyframes.txt` like

```sh 
 ffmpeg -copyts -i input_video \
-map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 \
-c:v libx264 -g 60 \
-force_keyframes keyframes.txt \
-c:a aac \
-filter:v:0 scale=w=480:h=360 -maxrate:v:0 600k -b:a:0 500k \
-filter:v:1 scale=w=640:h=480 -maxrate:v:1 1500k -b:a:1 1000k \
-filter:v:2 scale=w=1280:h=720 -maxrate:v:2 3000k -b:a:2 2000k \
-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2" \
-preset fast -f hls \
-hls_time 4 -hls_list_size 0 -hls_flags independent_segments \
-master_pl_name "master.m3u8" \
-y "%v/index.m3u8"
``` 

* ffmpeg will insert keyframes at your SCTE-35 splicepoints.
---

#### 3. Use x9k3 to insert scte35

* set segment times to match -hls_time you used in your ffmpeg command.
* your input is the ffmpeg master.m3u8 file from step 2.
* x9k3 will insert SCTE-35 from the sidecar file at the keyframes ffmpeg just inserted.
```sh
x9k3 -i master.m3u8 -t 4  -s sidecar.txt -o out_dir
```

  

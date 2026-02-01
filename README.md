
# x9k3 
# x9k3 Injects SCTE-35 Into HLS 

 # News of The World
 
* <s>I'm trying add support for injesting SRT streams. I have SRT working with threefive.the issue I'm having with x9k3 is disconnecting and reconnecting takes about 5 seconds longer that I want it to,
and I'm ironing that out.</s> __SRT support__ for input videos is now working.
* Expect a __new release__ with SRT support __by February__.
* __python 3.14__ makes changes to the default __multiprocessing spawn__ method, I __fixed__ that __in x9k3__ last night.
* __x9k3 runs perfectly on python3__, but __x9k3 runs best on pypy3__.  It's all about the __JIT__ man.



  _Adrian_


---
</samp>



# Current Version:  `v1.0.13`  _(02/3/2026)_ 
# `Features`

   * __All SCTE-35 HLS Tags__ are Supported.
   * __Add SCTE-35 Tags to ABR HLS__
   * __Segment MPEGTS streams into HLS and transfer SCTE-35 or add new SCTE-35 Tags__
   * __SCTE-35 Cues__ in __Mpegts Streams__ are Translated into __HLS tags__.
   * __SCTE-35 Cues can be added from a [Sidecar File](#sidecar-files)__.
   * Segments are __Split on SCTE-35 Cues__ as needed.
   * Segments __Start on iframes__.
   * Supports __h264__ and __h265__ .
   * __Multi-protocol.__ Input sources may be __Files, Http(s), Multicast, SRT, or Unicast UDP streams__.
   * Supports [__Live__](https://github.com/futzu/scte35-hls-x9k3#live) __Streaming__.

---

# Documentation

### Q. 
__What`s up with all the releases?__

### A.
 __Whenever I figure something out or fix a bug, I make a new release.__ I'm not going to make you wait for a bug fix. This way, releases are incremental, rather than  brand new software. Unless I have a really really good reason not to, I maintain backwards compatibilty and the interface, and by interface I mean function and method calls and such. New releases are designed to work with your existing code.<BR> __Sometimes I just make a stupid mistake doing the build and have to do a new one__.

* [Install](#install)
* Use 
    * [__Cli__](#cli)
      * [Switches](#switches) _( --this and --that)_
      * [__Usage__ Examples](#example-usage)  
    * [__Lib__](#programmatically) _(how to use x9k3 as a library)_
      * [ABR in Code](#abr-in-code)  
    * [__Sidecar Files__](#sidecar-files) _(these are how you add the SCTE-35, super important)_
      * [Adding SCTE-35 in real time](#in-live-mode-you-can-do-dynamic-cue-injection-with-a-sidecar-file)
      * [SCTE-35 Splice Immediate ](#sidecar-files-can-now-accept-0-as-the-pts-insert-time-for-splice-immediate) (_not the same as real time_)
      * __SCTE-35 Generation__ with [adbreak3](#adbreak3)
    * [__Playlists__](#playlists) _(make a playlist of MPEGTS or M3u8 files and feed it x9k3 as input)_
* HLS Stuff
    * [__HLS as Input__](#hls-as-input) 
    * [__ABR HLS__](#abr-hls) _(there are some terms and conditions)_
       * [ABR in Code](#abr-in-code) _(in less than ten lines)_
    * [__Byterange__ HLS](#byterange) 
    * [__Live__ HLS](#live) _(sliding windows, deleting segments, all that jazz)_
    * [__Looping__ videos](#--replay) _(play the same thing over and over)_
* [__Cues__](#cues)
    * [CUE-OUT](#cue-out) 
    * [CUE-IN](#cue-in)
* [SCTE-35 __Tags__](#supported-hls--tags)
    * [#EXT-X-CUE](#x_cue)
    * [__#EXT-X-SCTE35__](#x_scte35)
    * [#EXT-X-DATERANGE](#x_daterange)
    * [__#EXT-X-SPLICEPOINT__](#x_splicepoint)




# `Install`
* Use pip to install the the x9k3 lib and  executable script x9k3 (_will install threefive,m3ufu too_)
```lua
# python3

python3 -mpip install x9k3

# pypy3 

pypy3 -mpip install x9k3
```

[⇪ top](#documentation)

# `Details` 

*  __X-SCTE35__, __X-CUE__, __X-DATERANGE__, or __X-SPLICEPOINT__ HLS tags can be generated. set with the `--hls_tag` switch.

* reading from stdin now available
* Segments are cut on iframes.
* Segment time is 2 seconds or more, determined by GOP size. Can be set with the `-t` switch or by setting `X9K3.args.time` 
* Segments are named seg1.ts seg2.ts etc...
*  For SCTE-35, Video segments are cut at the the first iframe >=  the splice point pts.
*  If no pts time is present in the SCTE-35 cue, the segment is cut at the next iframe. 
* SCTE-35 cues with a preroll are inserted at the splice point.
* x9k3 can continue an existing m3u8 file. You can switch or resume streams, x9k3 handles the details.

# `How to Use`



# `cli`

### Switches
```smalltalk
a@fu:~/x9k3$ x9k3 --help

usage: x9k3 [-h] [-i INPUT] [-b] [-c] [-d] [-l] [-n]
            [-no_adrian_is_cool_tags_at_splice_points_because_I_suck] [-N]
            [-o OUTPUT_DIR] [-e] [-p] [-r] [-s SIDECAR_FILE] [-S] [-t TIME]
            [-T HLS_TAG] [-w WINDOW_SIZE] [-v]

optional arguments:

  -h, --help            show this help message and exit

  -i INPUT, --input INPUT
                        The Input video can be mpegts or m3u8 with mpegts
                        segments, or a playlist with mpegts files and/or
                        mpegts m3u8 files. The input can be a local video,
                        http(s), udp, multicast or stdin.

  -b, --byterange       Flag for byterange hls [default:False]

  -c, --continue_m3u8   Resume writing index.m3u8 [default:False]

  -d, --delete          delete segments (enables --live) [default:False]

  -l, --live            Flag for a live event (enables sliding window m3u8)
                        [default:False]

  -n, --no_discontinuity                 
                        Flag to disable adding #EXT-X-DISCONTINUITY tags at
                        splice points [default:False]

  -no_adrian_is_cool_tags_at_splice_points_because_I_suck
                        Flag to disable adding #EXT-X-ADRIAN-IS-COOL tags at
                        splice points [default:False]

  -N, --no-throttle, --no_throttle              
                        Flag to disable live throttling [default:False]

  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Directory for segments and index.m3u8(created if
                        needed) [default:'.']

  -e, --exclude_mpegts  Flag to exclude parsing SCTE-35 from MPEGTS.
                        [default:False]

  -p, --program_date_time
                        Flag to add Program Date Time tags to index.m3u8  [default:False]

  -r, --replay          Flag for replay aka looping (enables --live,--delete)
                        [default:False]

  -s SIDECAR_FILE, --sidecar_file SIDECAR_FILE
                        Sidecar file of SCTE-35 (pts,cue) pairs.
                        [default:None]

  -S, --shulga          Flag to enable Shulga iframe detection mode
                        [default:False]

  -t TIME, --time TIME  Segment time in seconds [default:2]

  -T HLS_TAG, --hls_tag HLS_TAG
                        x_scte35, x_cue, x_daterange, or x_splicepoint
                        [default:x_cue]

  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        sliding window size (enables --live) [default:5]

  -v, --version         Show version

```

### `Example Usage`

 #### `local file as input`
 ```smalltalk
    x9k3 -i video.mpegts
 ```
 #### `multicast stream as input with a live sliding window`   
   ```smalltalk
   x9k3 --live -i udp://@235.35.3.5:3535 -o output_dir
   ```
  #### Live mode works with a live source or static files.
  *  x9k3 will throttle segment creation to mimic a live stream.
   ```js
   x9k3 --live -i /some/video.ts -o output_dir
   ```
 #### `live sliding window and deleting expired segments`
   ```smalltalk
   x9k3  -i udp://@235.35.3.5:3535 --delete -o output_dir
   ```
#### `https stream for input, and writing segments to an output directory`
   *  directory will be created if it does not exist.
 ```smalltalk
   x9k3 -i https://so.slo.me/longb.ts --output_dir /home/a/variant0
 ```
#### `https hls m3u8 for input, and inserting SCTE-35 from a sidecar file, and continuing from a previously create index.m3u8 in the output dir`
 ```smalltalk
   x9k3 -i https://slow.golf/longb.m3u8 --output_dir /home/a/variant0 -continue_m3u8 -s sidecar.txt
 ```  
#### `using stdin as input`
   ```smalltalk
   cat video.ts | x9k3   -o output_dir
   ```
#### `live m3u8 file as input, add SCTE-35 from a sidecar file, change segment duration to 3 and output as live stream`
```smalltalk
x9k3 -i https://example.com/rendition.m3u8 -s sidecar.txt -t 3 -l -o output-dir
```
[⇪ top](#documentation)



# `Programmatically`

## `Up and Running in three Lines`

```smalltalk
        from x9k3 import X9K3            # 1
        x9 = X9K3('/home/a/cool.ts')     # 2
        x9.decode()                      # 3
```



#### Writing Code with x9k3

* you can get a complete set of args and the defaults like this

```js
from x9k3 import X9K3
x9 = X9K3()

>>>> {print(k,':',v) for k,v in vars(x9.args).items()}

input : <_io.BufferedReader name='<stdin>'>
continue_m3u8 : False
delete : False
live : False
no_discontinuity : False
no_throttle : False
output_dir : .
program_date_time : False
replay : False
sidecar_file : None
shulga : False
time : 2
hls_tag : x_cue
window_size : 5
version : False
```
*   or just
```lua
>>>> print(x9.args)

Namespace(input=<_io.BufferedReader name='<stdin>'>, continue_m3u8=False, delete=False, live=False, no_discontinuity=False, no_throttle=False, output_dir='.', program_date_time=False, replay=False, sidecar_file=None, shulga=False, time=2, hls_tag='x_cue', window_size=5, version=False)
```


* Setting  parameters

```js
from x9k3 import X9K3
x9 = X9K3()
```
*  `input source`

```smalltalk
x9.args.input = "https://futzu.com/xaa.ts"   
```
* `hls_tag` can be x_scte35, x_cue, x_daterange, or x_splicepoint

```smalltalk
x9.args.hls tag = x_cue 
```
* `output directory` default is "."
```js
x9.args.output_dir="/home/a/stuff"
```
* `live`
```smalltalk 
x9.args.live = True
```
* `replay` (loop video) ( also sets live )
```js
x9.args.replay = True
```
* `delete` segments when they expire ( also sets live )
```js
x9.args.delete = True
```

* add `program date time` tags ( also sets live )
```js
x9.args.program_date_time= True
```
* set `window size` for live mode ( requires live ) 
```js
x9.args.window_size = 5 
```
* run 
```js
x9.decode()
```

[⇪ top](#documentation)

### `HLS as input`
* x9k3 can use HLS manifests as input.
* HLS Must be MPEGTS with audio and video together in the segment.
* No audio only or separate audio.
* Existing HLS SCTE-35 Tags in input manifests will be dropped.
* [ABR HLS](#abr-hls) has additional restrictions

 ### `Byterange`
 * with the cli tool
    * use __full path to video file__  when creating byterange m3u8. 
```smalltalk
x9k3 -i /home/a/input.ts -b
```
* programmatically
```smalltalk
from x9k3 import X9K3
x9 = X9K3()
x9.self.args.byterange = True
x9.decode()
```
* output
```lua
#EXTM3U
#EXT-X-VERSION:4
#EXT-X-TARGETDURATION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-DISCONTINUITY-SEQUENCE:0
#EXT-X-X9K3-VERSION:0.2.55
#EXTINF:2.000000,
#EXT-X-BYTERANGE:135548@0
msnbc1000.ts
#EXTINF:2.000000,
#EXT-X-BYTERANGE:137992@135548
msnbc1000.ts
#EXTINF:2.000000,
#EXT-X-BYTERANGE:134796@273540
msnbc1000.ts
#EXTINF:2.000000,
#EXT-X-BYTERANGE:140436@408336
msnbc1000.ts
#EXTINF:2.000000,
#EXT-X-BYTERANGE:130096@548772
msnbc1000.ts
<SNIP>
```
[⇪ top](#documentation)

### `ABR HLS` 

__Here's how it works__. 
<samp>
* When x9k3 detects a master.m3u8 as input, it starts up an ABR instance.
* The ABR instance parses the master.m3u8 and finds rendtitions.
* For each rendition an x9k3 process is started.
* The ABR process also parses the SCTE-35 sidecar file and writes a sidecar file for each rendition.
* The master.m3u8 is written to the output_dir.
* Rendition segments and manifest files are written to output_dir/0, output_dir/1, etc.
* any args passed in are set for all rendtions.
</samp>
<img width="829" height="384" alt="image" src="https://github.com/user-attachments/assets/5a2e885f-44e0-42a6-a3d3-b524b4cb0758" />

 __The terms and condtions__.

* HLS version 3 support only
* Use a Sidecar file for SCTE-35 
* Only MPEGTS segments
* Audio and Video MUST be in the same stream.
* No separate Audio tracks
* No Audio only
* No WebVTT
* Pass a local master.m3u8 as input for x9k3
```sh
x9k3 -i ~/o21/master.m3u8 -t 3 -l -s sidecar.txt
```

* ABR works well over a network, if you have the bandwidth to download all renditions simultaneously.
     * If you don't have the bandwidth, the renditions will get out of sync.
     * The throttle time is a good indicator. throttle must be greater than half of target duration for all renditions.
     * throttle time is shown in the x9k3 output

```rebol
./0/seg0.ts:   start: 0.160   end: 10.000   duration: 9.840  # <-- duration   
throttling 8.22                        # <--- throttle time        throttle time > (duration / 2) GOOD


./2/seg0.ts:   start: 0.160   end: 10.000   duration: 9.840  # <-- duration  
throttling 4.23                       # <--- throttle time          throttle time < (duration / 2)  BAD

```

### `ABR in Code`
```py3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from x9k3 import argue
>>>> from x9k3.x9mp import do
>>>> url = 'https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8'
>>>> args = argue()
>>>> args.input=url
>>>> do(args)

```
* imports
```py3
from x9k3 import argue
from x9k3.x9mp import do
```
* define source
```py3
 url = 'https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8'

```
* generate  the args.
* [more about args](#writing-code-with-x9k3)
```py3

args = argue()
```
* args is the Namespace returned by the standard library's argparser.
* These are same options as the cli x9k3.
```py3
args
Namespace(input=<_io.BufferedReader name='<stdin>'>, byterange=False, continue_m3u8=False,
  delete=False, live=False, no_discontinuity=False, no_adrian_is_cool_tags_at_splice_points_because_I_suck=False,
  no_throttle=False, output_dir='.', exclude_mpegts=False,program_date_time=False, replay=False, sidecar_file=None,
  shulga=False, time=2, hls_tag='x_cue', window_size=5, version=False)
```
* use dot notation to set what you need
 ```py3
 args.input=url
```
* call do(args)
```py3
from x9k3.x9mp import do

```

* That's it.
   
[⇪ top](#documentation)


### `Playlists`
* playlists can be used as input
* playlist files must end in `.playlist`
* lines are  video or  video, sidecar
   * if video,sidecar, the sidecar file only applies to that video
* playlists can have mpegts video, mpegts m3u8, and playlists.
 
* example playlist
```lua
f10.ts,f10sidecar.txt # comments can be here
f17.ts
f60.ts
flat-striped.ts
# Comments can go here too.
flat.ts
input.ts
nmax.ts
nmx.ts,nmx-sidecar.txt
https://futzu.com/xaa.ts
https://example.com/index.m3u8,another-sidecar.txt
```
* using
```lua
 x9k3 -i out.playlist
```
[⇪ top](#documentation)


### `Sidecar Files`   
#### load scte35 cues from a Sidecar file

    
Sidecar Cues will be handled the same as SCTE35 cues from a video stream.   
line format for text file  `insert_pts, cue`
    
    
pts is the insert time for the cue, A four second preroll is standard. 
cue can be base64,hex, int, or bytes
     
  ```smalltalk
  a@debian:~/x9k3$ cat sidecar.txt
  
  38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ== 
  38199.918911, /DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm0= 

      
```
  ```smalltalk
  x9k3 -i  noscte35.ts  -s sidecar.txt 
  ```
##   In Live Mode you can do dynamic cue injection with a `Sidecar file`
   ```js
   touch sidecar.txt
   
   x9k3 -i vid.ts -s sidecar.txt -l 
   
   # Open another terminal and printf cues into sidecar.txt
   
   printf '38103.868589, /DAxAAAAAAAAAP/wFAUAAABdf+/+zHRtOn4Ae6DOAAAAAAAMAQpDVUVJsZ8xMjEqLYemJQ==\n' > sidecar.txt
   
   ```
## `Sidecar files` can now accept 0 as the PTS insert time for Splice Immediate. 
 
 

 Specify 0 as the insert time,  the cue will be insert at the start of the next segment.
 __Using 0 only works in live mode__

 ```js
 printf '0,/DAhAAAAAAAAAP/wEAUAAAAJf78A/gASZvAACQAAAACokv3z\n' > sidecar.txt

 ```
 [⇪ top](https://github.com/futzu/x9k3/blob/main/README.md#hls--scte35--x9k3)

 ##  A CUE-OUT can be terminated early using a `sidecar file`.

 
 In the middle of a CUE-OUT send a splice insert with the out_of_network_indicator flag not set and the splice immediate flag set.
 Do the steps above ,
 and then do this
 ```js
 printf '0,/DAcAAAAAAAAAP/wCwUAAAABfx8AAAEAAAAA3r8DiQ==\n' > sidecar.txt
```
 It will cause the CUE-OUT to end at the next segment start.
 ```js
#EXT-X-CUE-OUT 13.4
./seg5.ts:	start:112.966667	end:114.966667	duration:2.233334
#EXT-X-CUE-OUT-CONT 2.233334/13.4
./seg6.ts:	start:114.966667	end:116.966667	duration:2.1
#EXT-X-CUE-OUT-CONT 4.333334/13.4
./seg7.ts:	start:116.966667	end:118.966667	duration:2.0
#EXT-X-CUE-OUT-CONT 6.333334/13.4
./seg8.ts:	start:117.0	        end:119.0	duration:0.033333
#EXT-X-CUE-IN None
./seg9.ts:	start:119.3	        end:121.3	duration:2.3

``` 
 __Using 0 only works in live mode__
[⇪ top](#documentation)

   ---
## `Cues`   
   
##   `CUE-OUT`
#### A CUE-OUT is defined as:

* `A Splice Insert Command` with:
   *  the `out_of_network_indicator` set to `True` 
   *  a `break_duration`.
        
* `A Time Signal Command` and a Segmentation Descriptor with:
   *  a `segmentation_duration` 
   *  a `segmentation_type_id` of:
      * 0x22: "Break Start",
      * 0x30: "Provider Advertisement Start",
      * 0x32: "Distributor Advertisement Start",
      * 0x34: "Provider Placement Opportunity Start",
      * 0x36: "Distributor Placement Opportunity Start",
      * 0x44: "Provider Ad Block Start",
      * 0x46: "Distributor Ad Block Start",

[⇪ top](https://github.com/futzu/x9k3/blob/main/README.md#hls--scte35--x9k3)

## `CUE-IN`
#### A CUE-IN is defined as:
* `A Splice Insert Command`
  *  with the `out_of_network_indicator` set to `False`

* `A Time Signal Command` and a Segmentation Descriptor with:
   *  a `segmentation_type_id` of:

      * 0x23: "Break End",
      * 0x31: "Provider Advertisement End",
      * 0x33: "Distributor Advertisement End",
      * 0x35: "Provider Placement Opportunity End",
      * 0x37: "Distributor Placement Opportunity End",
      * 0x45: "Provider Ad Block End",
      * 0x47: "Distributor Ad Block End",

* For CUE-OUT and CUE-IN, `only the first Segmentation Descriptor will be used`
---
[⇪ top](#documentation)
    
## `Supported HLS  Tags`
* #EXT-X-CUE 
* #EXT-X-DATERANGE 
* #EXT-X-SCTE35 
* #EXT-X-SPLICEPOINT 

###  `x_cue`
* CUE-OUT
```lua
#EXT-X-DISCONTINUITY
#EXT-X-CUE-OUT:242.0
#EXTINF:4.796145,
seg32.ts
```
* CUE-OUT-CONT
```lua
#EXT-X-CUE-OUT-CONT:4.796145/242.0
#EXTINF:2.12,
```
* CUE-IN
```lua
#EXT-X-DISCONTINUITY
#EXT-X-CUE-IN
#EXTINF:5.020145,
seg145.ts

```
### `x_scte35`
* CUE-OUT
```lua
#EXT-X-DISCONTINUITY
#EXT-X-SCTE35:CUE="/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=" ,CUE-OUT=YES 
#EXTINF:4.796145,
seg32.ts
```
* CUE-OUT-CONT
```lua
#EXT-X-SCTE35:CUE="/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=" ,CUE-OUT=CONT
#EXTINF:2.12,
seg33.ts
```
* CUE-IN
```lua
#EXT-X-DISCONTINUITY
#EXT-X-SCTE35:CUE="/DAqAAAAAAAAAP/wDwUAAAKWf0//4rZw2AABAAAACgAIQ1VFSQAAAAAtegE5" ,CUE-IN=YES 
#EXTINF:5.020145,
seg145.ts
```
### `x_daterange`
* CUE-OUT
```lua
#EXT-X-DISCONTINUITY
#EXT-X-DATERANGE:ID="1",START-DATE="2022-10-14T17:36:58.321731Z",PLANNED-DURATION=242.0,SCTE35-OUT=0xfc302f00000000000000fff01405000002967fefffe16a1ab87e014c562000010000000a00084355454900000000ebf5a2a7
#EXTINF:4.796145,
seg32.ts
```
* CUE-IN
```lua
#EXT-X-DISCONTINUITY
#EXT-X-DATERANGE:ID="2",END-DATE="2022-10-14T17:36:58.666073Z",SCTE35-IN=0xfc302a00000000000000fff00f05000002967f4fffe2b670d800010000000a000
843554549000000002d7a0139
#EXTINF:5.020145,
seg145.ts
```

### `x_splicepoint`
* CUE-OUT
```lua
#EXT-X-DISCONTINUITY
#EXT-X-SPLICEPOINT-SCTE35:/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=
#EXTINF:4.796145,
seg32.ts
```
* CUE-IN
```lua
#EXT-X-DISCONTINUITY
#EXT-X-SPLICEPOINT-SCTE35:/DAqAAAAAAAAAP/wDwUAAAKWf0//4rZw2AABAAAACgAIQ1VFSQAAAAAtegE5
#EXTINF:5.020145,
seg145.ts

```
[⇪ top](#documentation)

## `VOD`

* x9k3 defaults to VOD style playlist generation.
* All segment are listed in the m3u8 file. 

## `Live`
* Activated by the `--live`, `--delete`, or `--replay` switch or by setting `X9K3.live=True`

### `--live`
   * Like VOD except:
     * M3u8 manifests are regenerated every time a segment is written
     * Segment creation is throttled when using non-live sources to simulate live streaming. ( like ffmpeg's "-re" )
     * default Sliding Window size is 5, it can be changed with the `-w` switch or by setting `X9k3.window.size` 
###  `--delete`
  * implies `--live`
  * deletes segments when they move out of the sliding window of the m3u8.
### `--replay`
  * implies `--live`
  * implies `--delete`
  * loops a video file and throttles segment creation to fake a live stream.

[⇪ top](#documentation)

   
### `adbreak3`

* included with x9k3
* adbreak3 is a cli tool to generate SCTE-35 for sidecar files.
* by default adbreak3 generates 2 SCTE35 Cues with Splice Inserts for CUE-OUT and CUE-IN and writes it to a sidecar file.

```sed
a@fu:~$ adbreak3 -h
usage: adbreak3 [-h] [-d DURATION] [-e EVENT_ID] [-i] [-o] [-p PTS] [-P] [-s SIDECAR] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        Set duration of ad break. [ default: 60.0 ]
  -e EVENT_ID, --event-id EVENT_ID
                        Set event id for ad break. [ default: 1 ]
  -i, --cue-in-only     Only make a cue-in SCTE-35 cue [ default: False ]
  -o, --cue-out-only    Only make a cue-out SCTE-35 cue [ default: False ]
  -p PTS, --pts PTS     Set start pts for ad break. Not setting pts will generate a Splice Immediate CUE-OUT. [default: 0.0 ]
  -P, --preroll         Add SCTE data four seconds before splice point. Used with MPEGTS. [ default: False ]
  -s SIDECAR, --sidecar SIDECAR
                        Sidecar file of SCTE-35 (pts,cue) pairs. [ default: sidecar.txt ]
  -v, --version         Show version
```
* Usage:
```rebol
a@fu:~$ adbreak3 --pts 1234.567890 --duration 30 --sidecar sidecar.txt

Writing to sidecar file: sidecar.txt

		CUE-OUT   PTS:1234.567889   Id:1   Duration: 30.0
		CUE-IN    PTS:1264.567889   Id:2
```

* Sidecar file has SCTE-35 Cues for CUE-OUT and CUE-IN

```smalltalk
a@fu:~$ cat sidecar.txt 
1234.56789,/DAlAAAAAAAAAP/wFAUAAABNf+/+Bp9rxv4AKTLgAE0AAAAAFz4v5A==
1264.56789,/DAgAAAAAAAAAP/wDwUAAABOf0/+BsiepgBOAAAAABSgtGA=
```

* Pass to x9k3
```rebol
x9k3 -i input.ts -s sidecar.txt

```
#### `Super Cool Feature`: adbreak3 can be used in real time to add SCTE-35 on the fly to live HLS manifest.


 






   ![image](https://github.com/futzu/x9k3/assets/52701496/65d915f9-8721-4386-9353-2e32911c6a64)

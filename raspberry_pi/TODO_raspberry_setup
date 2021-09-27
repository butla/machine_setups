Raspberry OS
=============

Steps (TODO)
------------

- increase video memory size
- get omxplayer to make sure hw-accelerated video can be played at all
- TODO compiling VLC
- setup the playback in chromium

Video quality
-------------

Increase Video memory size to 128 or 256 MB (sudo raspi-config)
Or just edit /boot/config.txt

omxplayer and kodi use hardware acceleration (through something called mmal?)

Chromium
--------

Źrodło: https://lemariva.com/blog/2020/08/raspberry-pi-4-video-acceleration-decode-chromium

Check chrome://gpu -> "Video Decode" option

chrome://flags -> enable
- Override software rendering list
- GPU rasterization
- Out of process rasterization
- Hardware-accelerated video decode (only available on the new versions of Raspberry Pi OS)

check chrome://media-internals/ while playing something to check if it worked

vsync tests are still showing tearing
- going down from 4k to 1080p and disabling pixel doubling didn't fix the tearing

You need to disable the compositor by
a) raspi-config/advanced options
b) sudo mv /etc/xdg/autostart/xcompmgr.desktop /home/pi/backup.xcompmgr.desktop
   sudo reboot

HW rendering
------------

test ffplay


Kodi
====

Kodi requires "Pulse default output device" as the audio output


TODO
====
- get hardware accelerated, fullscreen VLC on Raspberry OS.
  - is the VLC MMAL video output I see actually working?
  - compilation: https://www.techybugz.com/raspberry-pi/raspberry-pi-vlc/#/?playlistId=0&videoId=0
- audio, subtitle, and a progress bar in omxplayer?

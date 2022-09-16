Manjaro home RPI server, a playbook
===================================

## Initial setup

**get the image**
Image: Manjaro Minimal for RPI 4
https://github.com/manjaro-arm/rpi4-images/releases/download/22.06/Manjaro-ARM-minimal-rpi4-22.06.img.xz.torrent
https://manjaro.org/download/

**extract the image**
```
$ 7z x Manjaro-ARM-minimal-rpi4-22.06.img.xz
sudo dd if=Manjaro-ARM-minimal-rpi4-22.06.img of=/dev/sda bs=4M status=progress
```

**mount the created SD card**
mount sda2, ROOT_MNJRO, the filesystem from the SD card
It automounted in Manjaro, BTW.

**setup the wireless connection**
Info taken from [this post](https://forum.manjaro.org/t/guide-install-manjaro-arm-minimal-headless-on-rpi4-with-wifi/96515)

Put:
```
[Security]
Passphrase=YOUR WIFI PASSWORD GOES HERE
```

in this file: `/run/media/butla/ROOT_MNJRO/var/lib/iwd/<network_ssid>.psk`

**unmount the sdcard**

**scan the current status of your local network before turning RPI on**
`sudo nmap -sn 192.168.50.0/24 > nmap_before_rpi_boot`

**turn on the RPI**
Give it some time.

**see that RPI is up**
`sudo nmap -sn 192.168.50.0/24 > nmap_after_rpi_boot`

Compare the files, I use `meld` or `diff`: `meld nmap_before_rpi_boot nmap_after_rpi_boot`

The new thing is here:
```
Nmap scan report for 192.168.50.125
Host is up (0.065s latency).
MAC Address: <my RPI's MAC address> (Raspberry Pi Trading)
```

The RPIs address is 192.168.50.125 in this case.

**check if SSH is open on RPI**
`nmap 192.168.50.125`
I see that the SSH - port 22 - is there.

```
PORT   STATE SERVICE
22/tcp open  ssh
```

**SSH into the RPI, do the initial setup**
`ssh root@192.168.50.125`

Now you should see the TUI setup.

I set up a `butla` user, with a new password,
unique for the RPI (but one I can remember, 4 words), saved in my KeyPass.

**Continuation**

See `os_building_scripts/setup_rpi_manjaro_headless_server.sh`

### TODO

make neovim work. Maybe cut out some plugins that aren't working for RPI.
Now the thing is broken more than VIM, which is still a bit broken.

vim aliased to nvim (after nvim works more than vim)

### TODO: future, maybe
TODO copy the config files created by the setup TUI tool,
so I can just put them on the SD card directly after I create it.

TODO maybe I should've set up stuff in the SD card, maybe.

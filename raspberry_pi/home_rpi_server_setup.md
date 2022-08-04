Manjaro home RPI server, a playbook
===================================

## DONE
Image: Manjaro Minimal for RPI 4
https://github.com/manjaro-arm/rpi4-images/releases/download/22.06/Manjaro-ARM-minimal-rpi4-22.06.img.xz.torrent
https://manjaro.org/download/

```
$ 7z x Manjaro-ARM-minimal-rpi4-22.06.img.xz
sudo dd if=Manjaro-ARM-minimal-rpi4-22.06.img of=/dev/sda bs=4M status=progress
```

## TODO
- Connect over ethernet
  - first remember sudo nmap -sn 192.168.50.0/24
  - check again after connecting and turning on the RPI
  - compare results: `meld scan_1 scan_2`
  - found you:
  ```
  MAC Address: XX:XX:XX:XX:XX:XX (Raspberry Pi Trading)
  Nmap scan report for 192.168.50.184
  Host is up (0.034s latency).
  ```
  - no open ports, maybe I burned it wrong? Or maybe I need to put something on the SD card.
    More googling/duckduckgoing awaits.
  ```
  ❯ nmap 192.168.50.184
  Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-04 23:39 CEST
  Nmap scan report for 192.168.50.184
  Host is up (0.076s latency).
  All 1000 scanned ports on 192.168.50.184 are in ignored states.
  Not shown: 1000 closed tcp ports (conn-refused)

  Nmap done: 1 IP address (1 host up) scanned in 1.00 seconds
  ```
- connect to wifi
- pull `machine_setups`

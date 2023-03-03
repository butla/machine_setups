## Bloodlines

### TODOs
- make quick save / quick load work

### Setup
set proton 3-16.9 https://www.protondb.com/app/2600
add game -> non-steam -> pick unofficial patch. Run in directory - VTMB dir from steam

Run unofficial patch installer as an app in Steam
Select Path: Z:\home\butla\.local\share\Steam\steamapps\common\Vampire The Masquerade - Bloodlines

Set game launch options in steam: -full -game Unofficial_Patch

### Notes

**Hear the logos but can't skip them?**
Game launches in full screen but everything's black, and you hear the logos?
Press Alt+F4 once, and the logos should appear, and you'll be able to skip them with some button.

### More info
AUR: protontricks

protontricks --gui
use that to create a folder like
/home/butla/.local/share/Steam/steamapps/compatdata/2600

Follow this https://github.com/ValveSoftware/Proton/issues/1804#issuecomment-703183067:

### Maybe necessary???
Then, to run the unofficial patch run
WINEPREFIX=~/.local/share/Steam/steamapps/compatdata/2600/pfx wine VTMBup112rc5.3.exe


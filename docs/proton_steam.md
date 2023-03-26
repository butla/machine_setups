## Bloodlines

### TODOs
- make quick save / quick load work

### Setup
set proton 3-16.9 https://www.protondb.com/app/2600
add game -> non-steam -> pick unofficial patch. Run in directory - VTMB dir from steam

Run unofficial patch installer as an app in Steam
Select Path: Z:\home\butla\.local\share\Steam\steamapps\common\Vampire The Masquerade - Bloodlines

Set game launch options in steam: -full -game Unofficial_Patch

#### Keybindings
quick save - F5 (F9 crashes on proton)
quick load - unset
printscreen - f12 (TODO does that work, even?)
autorenew disciplines - on
stop disciplines - middle mouse button (works even on a touchpad)

### Notes

**Hear the logos but can't skip them?**
Game launches in full screen but everything's black, and you hear the logos?
Press Alt+F4 once, and the logos should appear, and you'll be able to skip them with some button.

**no screen after alt-tab out of the game**
Press alt+f4 when you're at the blank screen after alt-tabbing back into the game.
Something should happen, and you should be taken back to the game.

### More info
AUR: protontricks

protontricks --gui
use that to create a folder like
/home/butla/.local/share/Steam/steamapps/compatdata/2600

Follow this https://github.com/ValveSoftware/Proton/issues/1804#issuecomment-703183067:

### Maybe necessary???
Then, to run the unofficial patch run
WINEPREFIX=~/.local/share/Steam/steamapps/compatdata/2600/pfx wine VTMBup112rc5.3.exe


## Morrowind
Install from Steam with both Bloodmoon and Tribunal.

Then install mods (TODO figure this out):
- https://www.reddit.com/r/linux_gaming/comments/e78v9a/morrowind_mge_xe_mod_wine_or_proton/
- ??? https://gist.github.com/Magotchi/eb2c43c0d9aa1bd09817d5069c9fb680
- Morrowind code patch: https://www.nexusmods.com/morrowind/mods/19510
- Morrowind Rebirth: https://www.nexusmods.com/morrowind/mods/37795/

What about OpenMV? https://openmw.org/en/

### Increase fov:
/home/butla/.local/share/Steam/steamapps/common/Morrowind/Morrowind.ini
TODO - no option to set in vanilla, Morrowind, it seems.

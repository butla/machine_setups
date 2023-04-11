Proton games on Steam
=====================

## Don't use Steam from Flatpak

## Enabling Proton in Steam

[Top bar menu] -> Steam (first one) -> Settings -> Steam Play
  -> Advanced -> Enable Steam Play for all titles -> [Choose latest stable version]

## Vampire the Masquerade: Bloodlines (VtMB)
https://www.protondb.com/app/2600

### TODOs
- make quick save / quick load work on original keybindings (F9?)

### Setup
set proton 3-16.9

#### Install Bloodlines with Steam

#### Run the game to create prefix directory

#### Check the VtmB install folder in Steam local files

- Right click the game in library -> local files
- might look like this: 
  /home/USER/.steam/debian-installation/steamapps/common/Vampire The Masquerade - Bloodlines
  NOTE: use absolute paths in options

#### Unofficial Patch setup
add game [button below the games' list] -> non-steam
  -> browse [button below the list that can be loading] -> pick unofficial patch EXE file

Install `wine` package.

In unofficial patch properties:
- set run prefix
  WINEPREFIX=(absolute vtmb directory) wine VTMBup112rc5.3.exe
- Force compatibility tool - proton 3-16.9
  - this may be unavailable before restarting steam completely after first enabling Proton

Run the unofficial patch
- find the location of vampire.exe in your steam files:
  [steam library list] -> vtmb -> right-click -> properties -> local files -> etc.
- put that as absolute path as the input for the installer
- select options: "plus patch", "patch extra"

#### VtmB steam game properties

Run in directory - VTMB dir from steam

Force compatibility tool - proton 3-16.9
- this may be unavailable before restarting steam completely after first enabling Proton

Set game launch options in steam: -full -game Unofficial_Patch

#### Savegames sync with Syncthing
Saves are normally in a place like this, under the steam's "local files" directory
./.steam/debian-installation/steamapps/common/Vampire The Masquerade - Bloodlines/Unofficial_Patch/save/

Make that directory into a Syncthing directory

#### Keybindings
quick save - F5 (F9 crashes on proton)
quick load - unset
printscreen - f12 (TODO does that work, even?)
stop disciplines - middle mouse button (works even on a touchpad)

autorenew disciplines - off


### Notes

**Hear the logos but can't skip them?**
Game launches in full screen but everything's black, and you hear the logos?
Press Alt+F4 once, and the logos should appear, and you'll be able to skip them with some button.

**no screen after alt-tab out of the game**
Press alt+f4 when you're at the blank screen after alt-tabbing back into the game.
Something should happen, and you should be taken back to the game.

### More info
Source of knowledge: https://github.com/ValveSoftware/Proton/issues/1804#issuecomment-703183067:

THE BELOW MIGHT NOT BE NECESSARY:

AUR: protontricks

protontricks --gui
use that to create a folder like
/home/butla/.local/share/Steam/steamapps/compatdata/2600



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

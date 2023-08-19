Initial setup manual steps
==========================

Things to do
- Syncthing:
  - http://localhost:8384
  - "Actions" / Show ID
  - add the new device (with the shown ID) with the phone
  - set the phone as an introducer
  - set up folder shares (especially "documents" set up to "~/Documents") with the phone
  - set up GUI creds, run on HTTPS
- add id_rsa to ~/.ssh
- Brave:
  - enable sync (everything but passwords and open tabs)
  - set appearance (it's not synced... https://github.com/brave/brave-browser/issues/13555)
  - pinned cards
  - enable Trello integration in the Toggl Extension
  - don't warn about insecure certs from localhost: brave://flags/#allow-insecure-localhost
- Signal: sync with phone
- Dropbox: log in
- PIA: set it up - run `pia_download`, etc.
- Exodus wallet: go to "portfolio" screen, choose "restore from backup"
- qbittorrent
  - enable search:
    - View -> "search engine"
    - go to search panel, find "search plugins" button
  - right click the torrent list's column headers - add "completed date" - sort by it
- KeePassXC: log into the database, quit keepass with ctrl+q, so that it remembers the database
- set up ~/.credentials/borg_key from KeePass (chmod 600)
- copy files from "manually_linked" and "files_to_copy" (this should be done automatically in the future)
- `sudo systemctl enable --now sshd`
- check desktop environment doc for initial steps for it
- see "Graphics card setup" in [manjaro tricks](manjaro_tricks.md)

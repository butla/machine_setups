# RPI needs to have went through the initial configuration by now.

set -e

RPI_IP=$1

ssh-copy-id butla@$RPI_IP

# TODO The commands below don't run through fabric or mitogen yet, so this script isn't really usable,
# it's just a collection of commands to use.

# Would be nice to check when was the last time this ran. Or just put in my standard mirrors file, if it's not already
# there. Maybe a cron (anacron) that'd run this every week?
# sudo pacman-mirrors -f 

# Set locale:
# - uncomment en_GB.utf8 and pl_PL.UTF-8 in /etc/locale.gen
# - sudo locale-gen
# - copy locale.conf from "manually_linked" to /etc

# TODOs:
# - sshd config - have one for ognisko, bl, and bh?
# - pull `machine_setups`, run it

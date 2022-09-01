# RPI needs to have went through the initial configuration by now.

set -e

RPI_IP=$1

# adds my key to authorized_hosts
ssh-copy-id butla@$RPI_IP

# TODO The commands below don't run through fabric or mitogen yet, so this script isn't really usable,
# it's just a collection of commands to use.

# setup sshd_config / restart

# Would be nice to check when was the last time this ran. Or just put in my standard mirrors file, if it's not already
# there. Maybe a cron (anacron) that'd run this every week?
# sudo pacman-mirrors -f 

# Set locale:
# - uncomment en_GB.utf8 and pl_PL.UTF-8 in /etc/locale.gen
# - sudo locale-gen
# - copy locale.conf from "manually_linked" to /etc

# git clone git@github.com:butla/machine_setups  # could be done with HTTP
# cd machine_setups
# python3 -m workstation_setup

# TODOs:
# - RPI doesn't have pandoc package. Get rid of it from the package collection for ognisko. Why pandoc??
# - Warning: Could not load "/usr/lib/graphviz/libgvplugin_gtk.so.6" - It was found, so perhaps one of its dependents was not.  Try ldd.
# - apg is not available for aarch64

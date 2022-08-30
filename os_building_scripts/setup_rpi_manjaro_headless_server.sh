# RPI needs to have went through the initial configuration by now.

set -e

RPI_IP=$1

ssh-copy-id butla@$RPI_IP

# TODO maybe I should encode that with fabric or just mitogen?

# Would be nice to check when was the last time this ran. Or just put in my standard mirrors file, if it's not already
# there. Maybe a cron (anacron) that'd run this every week?
# sudo pacman-mirrors -f 

# sshd config - have one for ognisko, bl, and bh?

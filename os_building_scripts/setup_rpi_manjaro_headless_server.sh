# RPI needs to have went through the initial configuration by now.

set -e

RPI_IP=$1

ssh-copy-id butla@$RPI_IP

# sudo pacman-mirrors -f
# sudo systemctl enable --now avahi-daemon.service

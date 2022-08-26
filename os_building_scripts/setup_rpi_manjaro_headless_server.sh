# RPI needs to have went through the initial configuration by now.

set -e

RPI_IP=$1

ssh-copy-id butla@$RPI_IP

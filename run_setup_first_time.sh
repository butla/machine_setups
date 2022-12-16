#!/bin/bash

set -e

# TODO setup poetry when the code has dependencies

echo "----- Refreshing the the package mirrors... -----"
sudo pacman-mirrors -f
echo "----- Running the setup... -----"
python3 -m machine_setup

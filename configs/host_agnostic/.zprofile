# so that snap apps appear in my launcher
UBUNTU_SNAP_ENABLER=/etc/profile.d/apps-bin-path.sh
if [ -e $UBUNTU_SNAP_ENABLER ]; then
    emulate sh -c "source $UBUNTU_SNAP_ENABLER"
fi

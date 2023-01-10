"""
Functions to get info about the machine/computer we're running on.
"""

import os
import platform
import socket
from typing import Optional


def check_gui_present() -> bool:
    # TODO Have a better implementation for this.
    # Now it just excludes the only non-GUI machine in my setup.
    return not socket.gethostname() in ['ognisko']


def check_is_arm_cpu() -> bool:
    # This will work for the ognisko, which is an RPI4,
    # but can be expanded in the future.
    return platform.machine() == 'aarch64'


def get_desktop_environment() -> Optional[str]:
    # TODO do detection with some tool (inxi?) instead of an env var that doesn't work over SSH
    return os.environ.get('XDG_CURRENT_DESKTOP', '').lower()

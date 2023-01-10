"""
Functions to get info about the machine/computer we're running on.
"""

import platform
import socket


def check_gui_present() -> bool:
    # TODO Have a better implementation for this.
    # Now it just excludes the only non-GUI machine in my setup.
    return not socket.gethostname() in ['ognisko']


def check_is_arm_cpu() -> bool:
    # This will work for the ognisko, which is an RPI4,
    # but can be expanded in the future.
    return platform.machine() == 'aarch64'

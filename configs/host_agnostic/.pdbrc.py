"""
Config for pdbpp - a wrapper around pdb debugger.
"""

import pdb


class Config(pdb.DefaultConfig):
    sticky_by_default = True

Machine setups
==============

Code that sets up my computers with the software and configuration I want, and allows for them to stay in sync later.

You will also find the public part of my configuration and utility scripts in here.

How it works
------------

A Python program runs a bunch of shell commands to install and configure the software I want on a machine.
Also, it'll replace various configuration files with links to the config files in this repo's `configs` directory.

Rerunning the script will update the setup (packages, Git repos, plugins).

Usage
-----

To setup all the software and configuration or to update it later run the setup command from `Makefile` with `make`.

If you change any config file that's linked to this repo you can inspect and commit/revert the changes with Git.

If you want to fork this repository and adjust it for your purposes you might want to replace my private configs
repo in `.gitmodules`, or just remove the file altogether.
With that, you'll need to remove the line in Python code (from `machine_setup/config_links.py`)
that uses my private configs.

Docs
----

To check out some documentation, see `./docs`.

Similar tools
-------------

- [TJ DeVries's config_manager](https://github.com/tjdevries/config_manager)
- [chezmoi](https://www.chezmoi.io/)

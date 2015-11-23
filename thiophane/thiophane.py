#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import logging
import os
import sys

# load kanzo project script for thiophane
from kanzo import project
project.load(
    os.path.join(os.path.dirname(__file__), 'thtproject.py')
)

from kanzo.core import main as kanzo_main


def status_reporter(unit_type, unit_name, unit_status, additional=None):
    """Function for reporting installation state"""
    #TO-DO: finish this

@click.command()
@click.argument('cmd')
@click.option(
    '-d', '--debug',
    default=False,
    help=''
)
@click.option(
    '-l', '--log',
    default='~/.thiophane/installation.log',
    help=''
)
@click.option(
    '-t', '--timeout',
    default=300,
    help=''
)
@click.option(
    '-w', '--work-dir',
    default='~/.thiophane',
    help=''
)
def main(cmd, debug, log, timeout, work_dir):
    #TO-DO: setup logging handlers
    #TO-DO: load config file / generate config file
    config_path = None
    for key, value in project.__dict__.items():
        print("{key} - {value}".format(**locals()))

    kanzo_main.main(
        config_path,
        log_path=os.path.expanduser(log),
        debug=debug,
        timeout=timeout,
        reporter=status_reporter,
        work_dir=os.path.expanduser(work_dir)
    )


if __name__ == '__main__':
    main()

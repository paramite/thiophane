#!/usr/bin/env python3
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

from kanzo.conf import Config
from kanzo.core import controller
from kanzo.core import main as kanzo_main


DEFAULT_ANSWER_FILE_PREFIX = 'thiophane-answers'
DEFAULT_ANSWER_FILE = (
    './{0}-{1}.ini'.format(
        DEFAULT_ANSWER_FILE_PREFIX,
        project.PROJECT_RUN_TIMESTAMP
    )
)


def status_reporter(unit_type, unit_name, unit_status, additional=None):
    """Function for reporting installation state"""
    #TO-DO: finish this


@click.group()
@click.option(
    '-d', '--debug',
    default=False,
    help='run deployment in debug mode'
)
@click.pass_context
def cli(ctx, debug):
    ctx.obj['DEBUG'] = debug


@cli.command('gen-answer-file')
@click.argument('answer_file',
    default=DEFAULT_ANSWER_FILE
)
@click.pass_context
def generate_answer_file(ctx, answer_file):
    """Generates full answer file with default values."""
    config = controller.Controller.build_config_obj(answer_file)
    config.save()


@cli.command('answer-file')
@click.option(
    '-l', '--log',
    default='~/.thiophane/installation.log',
    help='log file path'
)
@click.option(
    '-t', '--timeout',
    default=300,
    help='maximum count of seconds each deployment step should take'
)
@click.option(
    '-w', '--work-dir',
    default='~/.thiophane',
    help='temporary directory for deployment files'
)
@click.argument('answer_file', required=False)
@click.pass_context
def run_with_answer_file(ctx, answer_file, log, timeout, work_dir):
    """Run deployment with given answer file. If none was given the latest
    one from current working directory is used.
    """
    # try to find latest answer file if none was given
    if not answer_file:
        try:
            answer_file = os.path.join(
                os.getcwd(),
                sorted([
                    i for i in os.listdir(os.getcwd())
                    if i.startswith(DEFAULT_ANSWER_FILE_PREFIX)
                ])[-1]
            )
            click.echo('Using answer file {0}'.format(answer_file))
        except IndexError:
            click.echo('No answer file was given and none was found in CWD.')
            sys.exit(1)

    kanzo_main.main(
        answer_file,
        log_path=os.path.expanduser(log),
        debug=ctx.obj['DEBUG'],
        timeout=timeout,
        reporter=status_reporter,
        work_dir=work_dir,
    )

@cli.command('all-in-one')
@click.pass_context
def run_with_answer_file(ctx):
    """Run default a.k.a all-in-one deployment."""
    generate_answer_file()
    run_with_answer_file()


def main():
    try:
        return cli(obj={})
    except KeyboardInterrupt:
        click.echo('Interrupted by user.')


if __name__ == '__main__':
    main()

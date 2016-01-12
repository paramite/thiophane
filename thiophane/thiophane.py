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
from kanzo.utils.shortcuts import normalize_path


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
    unit_name = unit_name.replace('_', ' ').capitalize()
    if unit_type == 'phase' and unit_status == 'start':
        caption = ' {unit_name} {unit_type} '.format(**locals())
        space = max(0, 80 - len(caption))
        click.echo(
            caption.ljust(
                len(caption) + int(space / 2), '='
            ).rjust(
                len(caption) + space, '='
            )
        )

@click.group()
@click.option(
    '-d', '--debug',
    is_flag=True,
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
@click.argument('answer_file', required=False)
@click.pass_context
def run_with_answer_file(ctx, answer_file, log, timeout):
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
    log = normalize_path(log)
    os.makedirs(os.path.dirname(log), mode=0o700, exist_ok=True)
    if not os.path.exists(log):
        os.close(os.open(log, mode=0o600))
    kanzo_main.main(
        answer_file,
        log_path=os.path.expanduser(log),
        debug=ctx.obj['DEBUG'],
        timeout=timeout,
        reporter=status_reporter,
    )

@cli.command('all-in-one')
@click.pass_context
def run_all_in_one(ctx):
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

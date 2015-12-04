# -*- coding: utf-8 -*-

"""Provision plugin

Plugin for preparing hosts for deployment.
"""

import click


def install_rdo_repo(shell, config, info, messages):
    click.echo('Installing RDO repository on host {0}'.format(shell.host))




#-------------------------------- plugin data ---------------------------------#
MODULES = []
RESOURCES = []
CONFIGURATION = [
    {'name': 'hosts/controller_hosts',
     'usage': 'List of hosts were to deploy API services',
     'is_multi': True,
     'default': 'localhost'},

    {'name': 'hosts/compute_hosts',
     'usage': 'List of hosts were to deploy hypervisor services',
     'is_multi': True,
     'default': 'localhost'},

    {'name': 'hosts/ceph_hosts',
     'usage': 'List of hosts were to deploy Ceph storage services',
     'is_multi': True,
     'default': 'localhost'},
]

INITIALIZATION = [install_rdo_repo]
PREPARATION = []
DEPLOYMENT = []
CLEANUP = []

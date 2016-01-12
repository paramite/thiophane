# -*- coding: utf-8 -*-

"""Provision plugin

Plugin for preparing hosts for deployment.
"""

import click
import greenlet
import re

from kanzo.utils.shell import execute

from thiophane.plugins.common import exceptions as tht_exceptions
from thiophane.plugins.common import processors as tht_processors


_RDO_REPO_VR = None
_RDO_REPO_URL = (
    'http://rdo.fedorapeople.org/openstack/openstack-{version}/'
    'rdo-release-{version}-{release}.rpm'
)


#------------------- initialization and preparation steps ---------------------#
def install_rdo_repo(shell, config, info, messages):
    """Installs RDO release repo RPM on all deployment hosts
    and enables testing repo in case it is required.
    """
    global _RDO_REPO_VR
    if not config['repos/install_rdo']:
        return
    # parsing installed RDO release on localhost: we want to proceed with this
    # only once
    if not _RDO_REPO_VR:
        click.echo('Parsed RDO release version: ', nl=False)
        rc, out, err = execute(
            "rpm -q rdo-release --qf='%{version}-%{release}.%{arch}\n'",
            use_shell=True,
        )
        match = re.match(
            r'^(?P<version>\w+)\-(?P<release>\d+\.[\d\w]+)\n',
            out
        )
        version, release = match.group('version'), match.group('release')
        _RDO_REPO_VR = (version, release)
        click.echo('{version}-{release}'.format(**locals()))
    else:
        version, release = _RDO_REPO_VR

    click.echo('Installing RDO release on host {0}'.format(shell.host))
    rdo_url = _RDO_REPO_URL.format(**locals())
    rc, out, err = shell.execute(
        '(rpm -q "rdo-release-{version}" || yum install -y --nogpg {rdo_url})'
        ' || true'.format(**locals())
    )

    # install RDO repo on all hosts first and then proceed with enabling
    # proper repo
    greenlet.getcurrent().parent.switch()
    click.echo('Enabling proper repo on host {0}'.format(shell.host))
    shell.execute('(rpm -q "yum-utils" || yum install -y yum-utils) || true')
    reponame = 'openstack-{}'.format(version)
    if config['repos/enable_rdo_testing']:
        cmd = 'yum-config-manager --enable {reponame}'
    else:
        cmd = (
            'yum-config-manager --disable {reponame}; '
            'yum-config-manager --enable {reponame}-testing'
        )
    rc, out, err = shell.execute(cmd.format(**locals()), can_fail=False)
    match = re.search('enabled\s*=\s*(1|True)', out)
    if not match:
        msg = (
            'Failed to enable proper RDO repo on host {shell.host}:\n'
            'RPM file seems to be installed, but appropriate repo file '
            'is probably missing in /etc/yum.repos.d/'.format(**locals())
        )
        raise tht_exceptions.PluginShellRuntimeError(
            msg, cmd=cmd, rc=rc, stdout=out, stderr=err
        )


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

    {'name': 'repos/install_rdo',
     'usage': 'Should RDO repo be installed?',
     'default': 'true',
     'options': [True, False],
     'processors': [
        tht_processors.bool_processor,
     ]},

    {'name': 'repos/enable_rdo_testing',
     'usage': 'Should RDO testing repo be enabled instead of stable repo?',
     'default': 'false',
     'options': [True, False],
     'processors': [
        tht_processors.bool_processor,
     ]},
]

INITIALIZATION = [install_rdo_repo]
PREPARATION = []
DEPLOYMENT = []
CLEANUP = []

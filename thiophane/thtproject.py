# -*- coding: utf-8 -*-

"""Thiophane project settings"""

import kanzo
import os


PROJECT_DIR = os.path.dirname(__file__)
PROJECT_NAME = 'Thiophane'
PROJECT_TEMPDIR = '/var/tmp/thiophane'
# please pardon a little hack
PROJECT_RUN_TIMESTAMP = kanzo.conf.defaultproject._timestamp
PROJECT_RUN_TEMPDIR = os.path.join(
    PROJECT_TEMPDIR, 'deployment-{0}'.format(PROJECT_RUN_TIMESTAMP)
)

# SSH connection settings
DEFAULT_SSH_USER = 'root'
DEFAULT_SSH_PORT = 22
DEFAULT_SSH_PRIVATE_KEY = '~/.ssh/id_rsa'

# SSH reconnect attempts count
SHELL_RECONNECT_RETRY = 3

# List of regular exceptions which are used to catch recognised errors from
# Puppet logs
PUPPET_ERRORS = [
    'err:', 'Syntax error at', '^Duplicate definition:', '^Invalid tag',
    '^No matching value for selector param', '^Parameter name failed:',
    'Error:', '^Invalid parameter', '^Duplicate declaration:',
    '^Could not find resource', '^Could not parse for', '^Could not autoload',
    '^/usr/bin/puppet:\d+: .+', '.+\(LoadError\)',
    '^\/usr\/bin\/env\: jruby\: No such file or directory'
]

# List of tuples. First item in tuple is regexp strings to match error,
# second item is message surrogate
# Example:
# PUPPET_ERROR_SURROGATES = [
#     ('Sysctl::Value\[.*\]\/Sysctl\[(?P<arg1>.*)\].*Field \'val\' is required',
#         'Cannot change value of %(arg1)s in /etc/sysctl.conf'),
# ]
PUPPET_ERROR_SURROGATES = []

# List of regexp strings to match errors which should be ignored
PUPPET_ERROR_IGNORE = []

# If Kanzo should try to apply all manifests even if one (or more) failed
# for some reason
PUPPET_FINISH_ON_ERROR = False

# List all possible commands how to install Puppet on hosts
PUPPET_INSTALLATION_COMMANDS = [
    'yum install -y puppet',      # Red Had based distros
    'apt-get install -y puppet',  # Debian based distros
]

# List all possible commands how to install Puppet and mis. dependencies
# on hosts.
PUPPET_DEPENDENCY_COMMANDS = [
    'yum install -y tar',      # Red Had based distros
    'apt-get install -y tar',  # Debian based distros
]

# Configuration files for Puppet
# Content variable host is internal variable.
# All other variables are formated from PUPPET_CONFIGURATION_VALUES dictionary
PUPPET_CONFIGURATION = [
    ('/etc/puppet/puppet.conf', PUPPET_CONFIG),
    ('/etc/puppet/hiera.yaml', HIERA_CONFIG),
]

# Values for Puppet configs. Values can be either static or dynamicaly glued
# from following variables:
# host - current host
# info - dictionary containing discovered info about current host
# config - loaded config values
# tmpdir - temporary directory on current host
PUPPET_CONFIGURATION_VALUES = {
    'datadir': '{tmpdir}/hieradata',
    'moduledir': '{tmpdir}/modules',
    'logdir': '{tmpdir}/logs',
}

# List of root directories where manifest fragments will be searched in.
PUPPET_MANIFEST_TEMPLATE_DIRS = [
    os.path.normpath(
        os.path.join(
            PROJECT_DIR,
            '..',
            'tripleo-heat-templates',
            'puppet',
            'manifests'
        )
    ),
    '/usr/share/openstack-tripleo-heat-templates/puppet/manifests',
]

# List of paths where project plugins are located
PLUGIN_PATHS = [
    os.path.join(PROJECT_DIR, 'plugins'),
]

# List of plugins which should be loaded
PLUGINS = [
    'provision',
    'tht',
    'final'
]

# We want to set logging, but all logging parameters will be set from CLI
SET_LOGGING = True

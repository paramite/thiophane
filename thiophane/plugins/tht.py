# -*- coding: utf-8 -*-

"""THT plugin

Plugin for application of Puppet manifests from tripleo-heat-templates
on deployment hosts.
"""

def validator(value, key, config):
    """..."""


def processor(value, key, config):
    """..."""


#-------------------------------- plugin data ---------------------------------#
CONFIGURATION = [
    {'name': 'section/parameter',
     'usage': '',
     'default': '',
     'options': [],
     'processors': [],
     'validators': []},
]

MODULES = []
RESOURCES = []
INITIALIZATION = []
PREPARATION = []
DEPLOYMENT = []
CLEANUP = []

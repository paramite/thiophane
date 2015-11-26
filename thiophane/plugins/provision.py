# -*- coding: utf-8 -*-

"""Provision plugin

Plugin for preparing hosts for deployment.
"""

PRIORITY = 0
CONFIGURATION = [
    {'name': 'hosts/controller_hosts',
     'usage': 'List of hosts were to deploy API services',
     'default': 'localhost'},

    {'name': 'hosts/compute_hosts',
     'usage': 'List of hosts were to deploy hypervisor services',
     'default': 'localhost'},

    {'name': 'hosts/ceph_hosts',
     'usage': 'List of hosts were to deploy Ceph storage services',
     'default': 'localhost'},
]
MODULES = []
RESOURCES = []
INITIALIZATION = []
PREPARATION = []
DEPLOYMENT = []
CLEANUP = []

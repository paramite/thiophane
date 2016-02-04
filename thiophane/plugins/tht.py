# -*- coding: utf-8 -*-

"""THT plugin

Plugin for application of Puppet manifests from tripleo-heat-templates
on deployment hosts.
"""

from kanzo.core.puppet import update_manifest


#------------------------- deployment planning steps --------------------------#
THT_CONTROLLER_STEP_COUNT = 6
THT_CONTROLLER_MANIFEST = 'overcloud_controller.pp'
THT_CONTROLLER_YAML = 'puppet/controller.yaml'


def controller_deployment_steps(config, info, messages):
    manifests = []
    for tht_step in range(THT_CONTROLLER_STEP_COUNT):
        step_template = 'controller_manifest_step{}'.format(tht_step),
        # create single-fragment manifest from controller manifest
        # in tripleo-heat-templates for each step
        # (step is passed in hiera file)
        update_manifest(
            step_template, THT_CONTROLLER_MANIFEST, hiera={'step': tht_step}
        )
        # each tht manifest is run several times over and over again with added
        # Puppet code, so we have to mimic this behaviour
        for host in config['hosts/controller_hosts']:
            marker = 'controller_{host}_{tht_step}'.format(**locals())
            prereqs = [
                'controller_{host}_{prev}'.format(host=host, prev=tht_step - 1)
            ]
            manifests.append(host, step_template, marker, prereqs)
    return manifests


#-------------------------------- plugin data ---------------------------------#
# TODO: automagically generate configuration from Heat template YAML
CONFIGURATION = [
]
MODULES = []
RESOURCES = []
INITIALIZATION = []
PREPARATION = []
DEPLOYMENT = []
CLEANUP = []

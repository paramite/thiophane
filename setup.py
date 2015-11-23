#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='thiophane',
    version='0.0.1',
    author='Martin Magr',
    author_email='martin.magr@gmail.com',
    description=(
        'OpenStack installation utility using Kanzo, Puppet '
        'and Puppet manifests from tripleo-heat-templates '
        '(a.k.a. THT - from which the project name comes from) '
        'to perform deployment steps.'
    ),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Kanzo',
    ],
    entry_points={
        'console_scripts': [
            'thiophane = thiophane.thiophane:main',
        ],
    }
)

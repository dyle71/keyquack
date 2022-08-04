#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
# setup.py
#
# keyquack setuptools main file
#
# (C) Copyright 2022, see the 'LICENSE' file in the project root.
# Oliver Maurhart, headcode.space, https://headcode.space
# ------------------------------------------------------------

from setuptools import setup


def requirements():
    with open('requirements.txt', 'rt') as f:
        return [line.strip() for line in f.readlines()]


setup(
    name='keyquack',
    version='0.1.0',
    description='Annoy your colleagues.',
    long_description='Annoy your colleagues in the office by making stupid '
                     'sounds at the keyboard while typing.',
    author='Oliver Maurhart',
    author_email='oliver.maurhart@headcode.space',
    maintainer='Oliver Maurhart',
    maintainer_email='oliver.maurhart@headcode.space',
    url='https://gitlab.com/dyle71/keyquack',
    license='MIT',

    # sources
    packages=['keyquack'],
    package_dir={'keyquack': 'src/keyquack'},
    scripts=['src/bin/keyquack'],

    # data
    include_package_data=True,
    data_files=[
        ('share/keyquack', ['requirements.txt',
                            'src/share/keyquack/boing.ogg',
                            'src/share/keyquack/moo.ogg',
                            'src/share/keyquack/quack.ogg'])
    ],

    install_requires=requirements()
)

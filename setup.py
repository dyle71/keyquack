#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------
# setup.py
#
# krydort setuptools main file
#
# This file is part of krydort.
#
# (C) Copyright 2020
# Oliver Maurhart, oliver.maurhart@headcode.space
# headcode.space e.U., https://www.headcode.space
# ------------------------------------------------------------

from setuptools import setup

import krydort

setup(
    name='krydort',
    version=krydort.__version__,
    description='Evaluation of different dicing game mechanics of the Witcher 3',
    long_description='This is just for fun: evaluation of different game mechanics '
                     'resolving a probe in the Witcher 3 tabel-top RPG'.
    author='Oliver Maurhart',
    author_email='oliver.maurhart@headcode.space',
    maintainer='Oliver Maurhart',
    maintainer_email='oliver.maurhart@headcode.space',
    url='https://www.github.com/dyle71/death-of-krydort',
    license='MIT',

    # sources
    packages=['krydort'],
    py_modules=[],
    scripts=['bin/krydort'],

    # data
    include_package_data=False,
    data_files=[
        ('share/krydort', ['requirements.txt'])
    ]
)

# SPDX-FileCopyrightText: 2024 The meson-python developers
#
# SPDX-License-Identifier: MIT

project('cmake-subproject', ['c', 'cpp', 'cython'], version: '1')

if meson.version().version_compare('>= 1.3.0')
    dep = dependency('cmaketest')
else
    dep = import('cmake').subproject('cmaketest').dependency('cmaketest')
endif

py = import('python').find_installation()

py.extension_module(
    'cmakesubproject',
    'cmakesubproject.pyx',
    dependencies: dep,
    override_options: ['cython_language=cpp'],
    install: true,
)

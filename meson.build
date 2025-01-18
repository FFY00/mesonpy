# SPDX-FileCopyrightText: 2021 The meson-python developers
#
# SPDX-License-Identifier: MIT

project('meson-python')

py = import('python').find_installation()

py.install_sources(
    'mesonpy/__init__.py',
    'mesonpy/_compat.py',
    'mesonpy/_editable.py',
    'mesonpy/_rpath.py',
    'mesonpy/_substitutions.py',
    'mesonpy/_tags.py',
    'mesonpy/_util.py',
    'mesonpy/_wheelfile.py',
    subdir: 'mesonpy',
)

# SPDX-FileCopyrightText: 2024 The meson-python developers
#
# SPDX-License-Identifier: MIT

project('symlinks', version: '1.0.0')

py = import('python').find_installation()

install_subdir(
  'subdir',
  install_dir: py.get_install_dir(pure: false),
)

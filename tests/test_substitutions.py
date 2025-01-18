# SPDX-FileCopyrightText: 2023 The meson-python developers
#
# SPDX-License-Identifier: MIT

import pytest

import mesonpy


def test_interpolate():
    assert mesonpy._substitutions.eval('$x ${foo}', {'x': 1, 'foo': 2}) == '1 2'


def test_interpolate_expression():
    assert mesonpy._substitutions.eval('${(x + 2 * 3 - 1) // 3 / 2}', {'x': 1}) == '1.0'


def test_interpolate_key_error():
    with pytest.raises(ValueError, match='unknown variable "y"'):
        mesonpy._substitutions.eval('$y', {'x': 1})


def test_interpolate_not_implemented():
    with pytest.raises(ValueError, match='invalid expression'):
        mesonpy._substitutions.eval('${x ** 2}', {'x': 1})


def test_substitutions(package_substitutions, monkeypatch):
    monkeypatch.setattr(mesonpy._substitutions, '_ncores', lambda: 2)
    with mesonpy._project() as project:
        assert project._meson_args['compile'] == ['-j', '3']


def test_substitutions_invalid(package_substitutions_invalid, monkeypatch):
    monkeypatch.setattr(mesonpy._substitutions, '_ncores', lambda: 2)
    with pytest.raises(mesonpy.ConfigError, match=''):
        with mesonpy._project():
            pass

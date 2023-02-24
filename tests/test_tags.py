# SPDX-FileCopyrightText: 2021 The meson-python developers
#
# SPDX-License-Identifier: MIT

import os
import pathlib
import platform
import sysconfig

from collections import defaultdict

import packaging.tags
import pytest

import mesonpy
import mesonpy._tags

from .conftest import adjust_packaging_platform_tag


# Test against the wheel tag generated by packaging module.
tag = next(packaging.tags.sys_tags())
ABI = tag.abi
INTERPRETER = tag.interpreter
PLATFORM = adjust_packaging_platform_tag(tag.platform)

SUFFIX = sysconfig.get_config_var('EXT_SUFFIX')
ABI3SUFFIX = next((x for x in mesonpy._EXTENSION_SUFFIXES if '.abi3.' in x), None)


def test_wheel_tag():
    assert str(mesonpy._tags.Tag()) == f'{INTERPRETER}-{ABI}-{PLATFORM}'
    assert str(mesonpy._tags.Tag(abi='abi3')) == f'{INTERPRETER}-abi3-{PLATFORM}'


@pytest.mark.skipif(platform.system() != 'Darwin', reason='macOS specific test')
def test_macos_platform_tag(monkeypatch):
    for minor in range(9, 16):
        monkeypatch.setenv('MACOSX_DEPLOYMENT_TARGET', f'10.{minor}')
        assert next(packaging.tags.mac_platforms((10, minor))) == mesonpy._tags.get_platform_tag()
    for major in range(11, 20):
        for minor in range(3):
            monkeypatch.setenv('MACOSX_DEPLOYMENT_TARGET', f'{major}.{minor}')
            assert next(packaging.tags.mac_platforms((major, minor))) == mesonpy._tags.get_platform_tag()


@pytest.mark.skipif(platform.system() != 'Darwin', reason='macOS specific test')
def test_python_host_platform(monkeypatch):
    monkeypatch.setenv('_PYTHON_HOST_PLATFORM', 'macosx-12.0-arm64')
    assert mesonpy._tags.get_platform_tag().endswith('arm64')
    monkeypatch.setenv('_PYTHON_HOST_PLATFORM', 'macosx-11.1-x86_64')
    assert mesonpy._tags.get_platform_tag().endswith('x86_64')


def wheel_builder_test_factory(monkeypatch, content):
    files = defaultdict(list)
    files.update({key: [(pathlib.Path(x), os.path.join('build', x)) for x in value] for key, value in content.items()})
    monkeypatch.setattr(mesonpy._WheelBuilder, '_wheel_files', files)
    return mesonpy._WheelBuilder(None, pathlib.Path(), pathlib.Path(), pathlib.Path(), {})


def test_tag_empty_wheel(monkeypatch):
    builder = wheel_builder_test_factory(monkeypatch, {})
    assert str(builder.tag) == 'py3-none-any'


def test_tag_purelib_wheel(monkeypatch):
    builder = wheel_builder_test_factory(monkeypatch, {
        'purelib': ['pure.py'],
    })
    assert str(builder.tag) == 'py3-none-any'


def test_tag_platlib_wheel(monkeypatch):
    builder = wheel_builder_test_factory(monkeypatch, {
        'platlib': [f'extension{SUFFIX}'],
    })
    assert str(builder.tag) == f'{INTERPRETER}-{ABI}-{PLATFORM}'


@pytest.mark.skipif(not ABI3SUFFIX, reason='Stable ABI not supported by Python interpreter')
def test_tag_stable_abi(monkeypatch):
    builder = wheel_builder_test_factory(monkeypatch, {
        'platlib': [f'extension{ABI3SUFFIX}'],
    })
    assert str(builder.tag) == f'{INTERPRETER}-abi3-{PLATFORM}'


@pytest.mark.skipif(not ABI3SUFFIX, reason='Stable ABI not supported by Python interpreter')
def test_tag_mixed_abi(monkeypatch):
    builder = wheel_builder_test_factory(monkeypatch, {
        'platlib': [f'extension{ABI3SUFFIX}', f'another{SUFFIX}'],
    })
    assert str(builder.tag) == f'{INTERPRETER}-{ABI}-{PLATFORM}'

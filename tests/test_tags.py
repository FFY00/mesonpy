# SPDX-License-Identifier: MIT

import os
import pathlib
import platform
import re
import sysconfig

from collections import defaultdict

import packaging.tags
import pytest

import mesonpy


tag = next(packaging.tags.sys_tags())
ABI = tag.abi
INTERPRETER = tag.interpreter
PLATFORM = mesonpy._adjust_manylinux_tag(tag.platform)
SUFFIX = sysconfig.get_config_var('EXT_SUFFIX')
ABI3SUFFIX = next((x for x in mesonpy._EXTENSION_SUFFIXES if '.abi3.' in x), None)


def wheel_builder_test_factory(monkeypatch, content):
    files = defaultdict(list)
    files.update({key: [(pathlib.Path(x), os.path.join('build', x)) for x in value] for key, value in content.items()})
    monkeypatch.setattr(mesonpy._WheelBuilder, '_wheel_files', files)
    return mesonpy._WheelBuilder(None, None, pathlib.Path(), pathlib.Path(), pathlib.Path(), pathlib.Path(), pathlib.Path())


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


@pytest.mark.skipif(platform.system() != 'Darwin', reason='macOS specific test')
def test_tag_macos_build_target(monkeypatch):
    monkeypatch.setenv('MACOS_BUILD_TARGET', '12.0')
    builder = wheel_builder_test_factory(monkeypatch, {
        'platlib': [f'extension{SUFFIX}'],
    })
    assert builder.tag.platform == re.sub(r'\d+\.\d+', '12.0', PLATFORM)

    monkeypatch.setenv('MACOS_BUILD_TARGET', '10.9')
    builder = wheel_builder_test_factory(monkeypatch, {
        'platlib': [f'extension{SUFFIX}'],
    })
    assert builder.tag.platform == re.sub(r'\d+\.\d+', '10.9', PLATFORM)

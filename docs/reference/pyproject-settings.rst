.. SPDX-FileCopyrightText: 2023 The meson-python developers
..
.. SPDX-License-Identifier: MIT

.. _reference-pyproject-settings:

****************
Project settings
****************

This page lists the configuration settings supported by
``meson-python`` in the ``pyproject.toml`` file. Please refer to the
:ref:`how-to-guides-meson-args` guide for for information on how to
use them and examples.

.. option:: tool.meson-python.limited-api

   A boolean indicating whether the extension modules contained in the
   Python package target the `Python limited API`__.  Extension
   modules can be compiled for the Python limited API specifying the
   ``limited_api`` argument to the |extension_module()|__ function
   in the Meson Python module.  When this setting is set to true, the
   value ``abi3`` is used for the Python wheel filename ABI tag.

   This setting is automatically reverted to false when the
   ``-Dpython.allow_limited_api=false`` option is passed to ``meson
   setup``.

.. option:: tool.meson-python.meson

   A string specifying the ``meson`` executable or script to use. If it is a
   path to an existing file with a name ending in ``.py``, it will be invoked
   as a Python script using the same Python interpreter that is used to run
   ``meson-python`` itself. It can be overridden by the :envvar:`MESON`
   environment variable.

.. option:: tool.meson-python.shared-libs-win32

   A boolean indicating whether shared libraries should be supported on
   Windows. ``meson-python`` installs shared libraries in a dedicated location
   and uses RPATH or equivalent mechanisms to have Python modules and native
   executables load them form there. Windows does not have an equivalent
   mechanism to set the DLL load path. Supporting shared libraries on Windows
   requires collaboration from the package. To make sure that package authors
   are aware of this requirement, ``meson-python`` raises an error if a
   package contains DLLs and this option is not set.

.. option:: tool.meson-python.args.dist

   Extra arguments to be passed to the ``meson dist`` command.

.. option:: tool.meson-python.args.setup

   Extra arguments to be passed to the ``meson setup`` command.

.. option:: tool.meson-python.args.compile

   Extra arguments to be passed to the ``ninja`` command.

.. option:: tool.meson-python.args.install

   Extra arguments to be passed to the ``meson install`` command.


__ https://docs.python.org/3/c-api/stable.html?highlight=limited%20api#stable-application-binary-interface
__ https://mesonbuild.com/Python-module.html#extension_module

.. |extension_module()| replace:: ``extension_module()``

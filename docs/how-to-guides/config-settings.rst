.. SPDX-FileCopyrightText: 2023 The meson-python developers
..
.. SPDX-License-Identifier: MIT

.. _how-to-guides-config-settings:

***************************
Using build config settings
***************************

Build config settings can be used to customize some aspects of the
build. See the :doc:`../reference/config-settings` reference for a list
of the settings implemented by ``meson-python``.

How build config settings are specified depends on the Python package
build front-end used. The most popular build front-end are `build`_ and
`pip`_. These use the ``--config-settings`` long command line option or
the ``-C`` short command line option:

.. tab-set::

    .. tab-item:: pypa/build
        :sync: key_pypa_build

	.. code-block:: console

	   $ python -m build --wheel \
               -Csetup-args="-Doption=true" \
               -Csetup-args="-Dvalue=1" \
               -Ccompile-args="-j6"

    .. tab-item:: pip
        :sync: key_pip

	.. code-block:: console

       $ # note: pip >=23.1 also accepts -C instead of --config-settings
	   $ python -m pip wheel . \
               --config-settings=setup-args="-Doption=disable" \
               --config-settings=compile-args="-j6"


Refer to the `build`_ and `pip`_ documentation for details.  This
example uses the ``python -m pip wheel`` command to build a Python wheel
that can be later installed or distributed. To build a package and
immediately install it, replace ``wheel`` with ``install``.  See the
:ref:`how-to-guides-meson-args` guide for more examples.


.. admonition:: Passing multiple settings
   :class: caution

   Please note that ``pip`` prior to 23.1 did not offer a way to set a
   build config setting to a list of strings: later values for the
   same key passed to ``--config-settings`` override earlier ones,
   effectively limiting the number of options that can be passed to
   each command invoked in the build process to one. This limitation
   has been lifted in ``pip`` release 23.1.


.. _build: https://pypa-build.readthedocs.io/en/stable/
.. _pip: https://pip.pypa.io/


Using a persistent build directory
==================================

By default, ``meson-python`` uses a temporary build directory which is
deleted when the build terminates. A persistent build directory allows
faster incremental builds and to access build logs and intermediate
build artifacts. The ``build-dir`` :ref:`config setting
<reference-config-settings>` instructs ``meson-python`` to use a
user-specified build directory which will not be deleted. For example:

.. tab-set::

    .. tab-item:: pypa/build
        :sync: key_pypa_build

	.. code-block:: console

	   $ python -m build -Cbuild-dir=build

    .. tab-item:: pip
        :sync: key_pip

	.. code-block:: console

	   $ python -m pip install . -Cbuild-dir=build

After running this command, the ``build`` directory will contain all
the build artifacts and support files created by ``meson``, ``ninja``
and ``meson-python``.  The same build directory can be used by
subsequent invocations of ``meson-python``, avoiding the need to
rebuild the whole project when testing changes during development.

Using a permanent build directory also aids in debugging a failing
build by allowing access to build logs and intermediate build outputs,
including the Meson introspection files and detailed log. The latter
is stored in the ``meson-logs/meson-log.txt`` file in the build
directory and can be useful to diagnose why a build fails at the
project configuration stage. For example, to understand why dependency
detection failed, it is often necessary to look at the ``pkg-config``
or other dependency detection methods output.

Access to detailed logs and intermediate build outputs is particularly
helpful in CI setups where introspecting the build environment is
usually more difficult than on a local system. Therefore, it can be
useful to show the more detailed log files when the CI build step
fails. For example, the following GitHub Actions workflow file snippet
shows the detailed Meson setup log when the build fails:

.. code-block:: yaml

    - name: Build the package
      run: python -m build --wheel -Cbuild-dir=build
    - name: Show meson-log.txt
      if: failure()
      run: cat build/meson-logs/meson-log.txt

Replacing ``failure()`` with ``always()`` in the code above will
result in the Meson log file always being shown. See the GitHub
Actions documentation__ for more details. Please be aware that the
setup log can become very long for complex projects, and the GitHub
Actions web interface becomes unresponsive when the running job emits
many output lines.


__ https://docs.github.com/en/actions/learn-github-actions/expressions#status-check-functions

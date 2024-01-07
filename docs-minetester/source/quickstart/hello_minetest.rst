Hello, Minetester!
==================

To get started with Minetester you should first know your way around the directory structure.
The most important directories are these:

.. code-block:: yaml

    minetest/
    ├── bin             # contains minetest executable
    ├── clientmods      # contains client-side mods
    ├── doc             # contains documentation
    ├── docs-minetester # contains Minetester documentation
    ├── games           # contains games (vanilla Minetest by default)
    ├── log             # contains log files
    ├── mods            # contains server-side mods
    ├── minetester      # contains Minetester Python module
    ├── scripts         # contains utility scripts
    └── src             # contains C++ source code 


Executing Minetest
------------------

You can jump directly into a single player game (skipping the main menu) by running

.. code-block:: bash

    ./bin/minetest --go

Internally, this command starts a server and a client on your computer and connects them to each other.

There are many more command line options available. You can find them by running

.. code-block:: bash

    ./bin/minetest --help

For example, you can start a server and a client separately by running these commands in different terminals:

.. code-block:: bash

    ./bin/minetest --server
    ./bin/minetest --address 0.0.0.0 --port 30000 --go --name Bob

A powerful way to modify Minetest is to pass a configuration file (see `minetest.conf.example <minetest_conf_dummy.html>`_ for available options):

.. code-block:: bash

    ./bin/minetest --config minetest.conf

Minetester command line options
-------------------------------

.. list-table::
   :widths: 1 2
   :header-rows: 1

   * - Minetester CLI Option
     - Description
   * - ``--dumb``
     - Start a dumb client that can receive actions from and return observations to an external controller client.
   * - ``--record``
     - Start a recording client that returns observations to an external data gathering client.
   * - ``--client-address``
     - Address to the controller / data gathering client.
   * - ``--headless``
     - Start client in headless mode.
   * - ``--sync-port``
     - Internal port used for syncing server and clients.
   * - ``--sync-dtime``
     - Ingame time difference between steps when using server-client synchronization.
   * - ``--noresizing``
     - Disallow screen resizing.
   * - ``--cursor-image``
     - Path to cursor image file that is rendered at the mouse position in the dumb client mode.

Below we focus on connecting a **server**, a **dumb client** and `Minetester's gymnasium environment. <../_api/minetester.minetest_env.html#minetester.minetest_env.Minetest>`_

To learn more about the other CLI options please refer to the :ref:`tutorials <tutorials>`.

Sending random actions
----------------------

Let's manually start a server and a dumb client via

.. code-block:: bash

    # remember how a server is started internally in singleplayer?
    ./bin/minetest --go --dumb --client-address "tcp://localhost:5555"


We can set up a little Python script that acts as controller client using :py:class:`minetester.minetest_env.Minetest`,
which implements the gymnasium environment interface.

.. literalinclude:: random_controller_loop.py
   :language: python
   :linenos:

Make sure to provide matching ports in ``--client-address`` and ``env_port`` for connecting to the Minetest client.
Running this script should pop up two windows: one from the Minetest client and one from the Python controller rendering a randomly acting player.

.. note::

  By default ``start_minetest=True`` such that server and dumb client are started automatically as subprocesses.

Further resources about Minetest
--------------------------------

- `minetest.net <https://minetest.net>`_
- `Minetest Wiki <https://wiki.minetest.net>`_
- `Minetest Forum <https://forum.minetest.net>`_
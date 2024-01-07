What is Minetester?
===================

Minetester extends the open-source voxel engine `Minetest <https://www.minetest.net/>`_ to support training and evaluation of AI / RL agents.
The Minetest core was modified to add the following main features:

- a dumb client that adds an `API for controlling a player and receiving game information <../advanced/client_api.html>`_
- support for `custom tasks using the Minetest modding API <../tutorials/create_task.html>`_
- `headless client operation <../tutorials/headless_mode.html>`_
- `client-server synchronization <../tutorials/synchronization.html>`_

In addition, the :py:mod:`minetester` Python package provides a gymnasium environment and utilities for communication with Minetest clients.

For a motivation of the project, see the introductory `blog post <https://blog.eleuther.ai/minetester-intro/>`_.

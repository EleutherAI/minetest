How to create a new task?
================================

Tasks are easy to create using Minetest's builtin Lua modding API. 
The task-relevant information (rewards, task completion status, meta information, ...) are passed through
the Minetest processes and made available to the `client API <../advanced/client_api.html>`_.

Task definition
---------------

A basic Minetest mod is defined by a directory with the following structure

.. code-block::

    my_task\
        mod.conf
        init.lua
        settingtypes.txt

where `mod.conf` contains meta data, `init.lua` the necessary Lua code, and `settingtypes.txt` possible mod settings.
It is either located in  the **clientmods** or the **mods** directory (see :ref:`below <client_server_mods>`).

A task has to define or modify the following two global variables in the Lua script environment:

1. ``REWARD``: a scalar floating point number indicating the reward received at the current step.
2. ``TERMINAL``: a boolean indicating whether the agent has reached a terminal state of the task.

The variables can be changed at every step, or based on in-game events.

.. note:: 

    In order to avoid multiple definitions of ``REWARD`` and ``TERMINAL`` when using multiple task mods together,
    there is a default mod called **rewards** (see `client-side rewards mod <https://github.com/EleutherAI/minetest/tree/develop/clientmods/rewards>`_,
    `server-side rewards mod <https://github.com/EleutherAI/minetest/tree/develop/mods/rewards>`_) that takes care of the definition. If a mod with this name is found,
    it will be automatically loaded.

Example: A simple treechop task
-------------------------------

The following files define a simple task, ``treechop-v0``, that rewards chopping trees and terminates after
a certain number of tree nodes have been chopped.

`mod.conf`

.. literalinclude :: ../../../clientmods/treechop_v0/mod.conf
    :language: text
    :linenos:

`settingtypes.txt`

.. literalinclude :: ../../../clientmods/treechop_v0/settingtypes.txt
    :language: text
    :linenos:

`ìnit.lua`

.. literalinclude :: ../../../clientmods/treechop_v0/init.lua
    :language: lua
    :linenos:

.. _client_server_mods:

Client and server mods
----------------------

Minetest provides two mod types, client-side mods located in the **clientmods** directory and server-side mods located in **mods**.

In the default, asynchronous client-server operation tasks are specified as client-side mods, meaning each client
tracks its own reward and task termination variables.
One downside of client-side mods is that they don't have access to all information that is available on the server-side,
e.g. the inventory of the player.
In order to still obtain this information one can have an additional server-side mod and make use of so-called **mod channels**
to communicate the required data (see ``treechop-v1``: `client-side <https://github.com/EleutherAI/minetest/tree/develop/clientmods/treechop_v1>`_,
`server-side <https://github.com/EleutherAI/minetest/tree/develop/mods/treechop_v1>`_).

On the other hand, when using `client-server synchronization <synchronization.html>`_, task data is distributed to the client
via the synchronization channel, such that **it is required** to exclusively use server mods for the task definition.
In this case, ``REWARD`` and ``TERMINAL`` are each tables of floats and booleans, respectively, containing values for each player name
(see ``treechop-v2``: `server-side only <https://github.com/EleutherAI/minetest/tree/develop/mods/treechop_v2>`_) 

Further resources
-----------------

- `Minetest Modding API Reference <https://minetest.gitlab.io/minetest/>`_
- `Minetest Modding Forum <https://forum.minetest.net/viewforum.php?f=46&sid=c43ec11858a985a18618026196a4d794>`_
Installation
============

Building submodules, minetest and minetester
--------------------------------------------

Follow the build instructions:

.. literalinclude:: ../../../build_instructions.txt
    :language: bash

You should see a window pop up with a player performing random actions in Minetest.

To clean build artifacts run:

.. code-block:: bash

    make clean

Rebuilding minetester
---------------------

Use the following instructions to only rebuild minetester (not minetest):

.. code-block:: bash

    make clean_minetester
    make minetester
    make install
    make demo
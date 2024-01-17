Headless modes
==============

There are two different modes, one using virtual framebuffer X server (`Xvfb <https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml>`_) and one using SDL2's offscreen mode.

Xvfb
~~~~
In order to use the Xvfb headless mode, before starting the Minetest client, a new virtual framebuffer X server has to be started at an unused display number.
You can either use the Xvfb CLI:

.. code-block:: bash
    
    export DISPLAY=:4
    export DISPLAY_WIDTH=1024
    export DISPLAY_HEIGHT=600
    export DISPLAY_DEPTH=24
    Xvfb $DISPLAY -screen 0 ${DISPLAY_WIDTH}x${DISPLAY_HEIGHT}x${DISPLAY_DEPTH}
    
or this Python utiltity: :py:func:`minetester.utils.start_xserver`


In addition, the ``--headless`` runtime flag has to be passed to the Minetest client, e.g.

.. code-block:: Python

    from minetester import Minetest
    env = Minetest(headless=True)

For convenience you can also tell the Minetest gym environment to start a Xvfb server:

.. code-block:: Python

    from minetester import Minetest
    env = Minetest(start_xvfb=True, headless=True)

SDL2 offscreen mode
~~~~~~~~~~~~~~~~~~~

Using the SDL2-based headless mode requires compilation with the following build flags

``-DBUILD_HEADLESS=1 -DSDL2_DIR=<path to SDL repo>/SDL/build/lib/cmake/SDL2/``

It also requires the ``--headless`` runtime flag to be passed to the Minetest client.
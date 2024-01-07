Client-server synchronization
=============================


Motivation
----------
Solid support of client-server synchronization is useful because of the following reasons:

1. reproducibility of experiments
    a. elimination of latency related differences in game state
    b. direct loading of missing chunks (additional thread of the server)
2. eliminating communication overhead in the single-agent setting by running client and server in the same process
3. global shared game state in multi-agent setting


Current implementation
----------------------

The current implementation of client-server synchronization only covers case 1. a. and can be considered an experimental feature.
Instead of running the server process asynchronously it adds a message queue between client and server to operate them in lock step.
It makes the following assumption:

- single agent (client)
- both processes run on the same machine
- task is specified in a server mod (see `task tutorial <create_task.html>`_)

There are two CLI arguments that need to be configured to make use of synchronization:

1. ``--sync-port``: Internal port used for syncing server and client. Make sure to pass the same port to both processes.
2. ``--sync-dtime``: Ingame time difference between steps when using server-client synchronization. For example, sync-dtime = 0.05 seconds => 20 steps per second. The default walking speed in Minetest is 4 nodes / second, i.e. 0.2 nodes / step for this setting of sync-dtime.
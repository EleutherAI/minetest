Client API
==========

The API provided for controlling and reading out the Minetest client is based on two libraries:

- `Protocol Buffers <https://protobuf.dev/>`_
- `ZeroMQ <https://zeromq.org/>`_

Protobuf objects are used for serializing and deserializing the messages, that are being sent using ZeroMQ.

Protobuf objects
----------------

The objects are defined in `/proto/objects.proto <https://github.com/EleutherAI/minetest/blob/develop/proto/objects.proto>`_.
The Minetest client receives ``Action`` messages and sends out ``Observation`` messages.

By default the Protobuf objects are compiled for C++ and Python using the
`/scripts/compile_proto.sh <https://github.com/EleutherAI/minetest/blob/develop/scripts/compile_proto.sh>`_ script.
This can be easily adjusted to compile for other languages.

ZeroMQ message patterns
-----------------------

There are two differnt ZeroMQ messaging patterns in use depending on the type of the client:

- dumb Minetest client <-> controller client: ``REQ/REP``

  In each step the dumb client sends a blocking request containing an observation to the controller
  which awaits the request and replies with an action.
- recording Minetest client <-> data gathering client : ``PUB/SUB``

  In each step the recording client publishes an observation and the data gathering client
  subscribes to the topic in order to read out the observations.
  See `this script <https://github.com/EleutherAI/minetest/blob/develop/scripts/data_recorder.py>`_
  for an example of how to implement a data gathering client.

In both cases the ZMQ socket address is passed to the Minetest client via the ``--client-address`` command line argument.

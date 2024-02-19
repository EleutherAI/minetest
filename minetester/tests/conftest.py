import os

import pytest


@pytest.fixture
def unused_xserver_number():
    """Get unused X server number."""
    for servernum in range(0, 65536):
        if os.path.exists("/tmp/.X{0}-lock".format(servernum)):
            continue
        else:
            return servernum

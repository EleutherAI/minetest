"""Utility functions for Minetester."""
import os
import subprocess
from typing import Any, Dict, Tuple

import numpy as np

from minetester.proto import objects_pb2 as pb_objects
from minetester.proto.objects_pb2 import KeyType

# Define default keys / buttons
KEY_MAP = {
    "FORWARD": KeyType.FORWARD,
    "BACKWARD": KeyType.BACKWARD,
    "LEFT": KeyType.LEFT,
    "RIGHT": KeyType.RIGHT,
    "JUMP": KeyType.JUMP,
    "SNEAK": KeyType.SNEAK,  # shift key in menus
    "DIG": KeyType.DIG,  # left mouse button
    "MIDDLE": KeyType.MIDDLE,  # middle mouse button
    "PLACE": KeyType.PLACE,  # right mouse button
    "DROP": KeyType.DROP,
    "HOTBAR_NEXT": KeyType.HOTBAR_NEXT,  # mouse wheel up
    "HOTBAR_PREV": KeyType.HOTBAR_PREV,  # mouse wheel down
    "SLOT_1": KeyType.SLOT_1,
    "SLOT_2": KeyType.SLOT_2,
    "SLOT_3": KeyType.SLOT_3,
    "SLOT_4": KeyType.SLOT_4,
    "SLOT_5": KeyType.SLOT_5,
    "SLOT_6": KeyType.SLOT_6,
    "SLOT_7": KeyType.SLOT_7,
    "SLOT_8": KeyType.SLOT_8,
    "INVENTORY": KeyType.INVENTORY,
}
INV_KEY_MAP = {value: key for key, value in KEY_MAP.items()}

# Define noop action
NOOP_ACTION = {key: 0 for key in KEY_MAP.keys()}
NOOP_ACTION.update({"MOUSE": np.zeros(2, dtype=int)})


def unpack_pb_obs(
    received_obs: str,
) -> Tuple[np.ndarray, float, bool, Dict[str, Any], Dict[str, int]]:
    """Unpack a protobuf observation received from Minetest client.

    Note: here 'observation' encompasses all information received from the client
    within one step and should not be confused with the observation
    returned by a gym environment.

    Args:
        received_obs: The received observation.

    Returns:
        The displayed image, task reward, done flag, info dict and last action.
    """
    pb_obs = pb_objects.Observation()
    pb_obs.ParseFromString(received_obs)
    obs = np.frombuffer(pb_obs.image.data, dtype=np.uint8).reshape(
        pb_obs.image.height,
        pb_obs.image.width,
        3,
    )
    last_action = unpack_pb_action(pb_obs.action) if pb_obs.action else None
    rew = pb_obs.reward
    done = pb_obs.terminal
    # TODO receive extra infos
    info = {}
    return obs, rew, done, info, last_action


def unpack_pb_action(pb_action: pb_objects.Action) -> Dict[str, int]:
    """Unpack a protobuf action.

    Args:
        pb_action: The protobuf action.

    Returns:
        The unpacked action as dictionary.
    """
    action = dict(NOOP_ACTION)
    action["MOUSE"] = [pb_action.mouseDx, pb_action.mouseDy]
    for key_event in pb_action.keyEvents:
        if key_event.key in INV_KEY_MAP and key_event.eventType == pb_objects.PRESS:
            key_name = INV_KEY_MAP[key_event.key]
            action[key_name] = 1
    return action


def pack_pb_action(action: Dict[str, Any]) -> pb_objects.Action:
    """Pack a protobuf action.

    Args:
        action: The action as dictionary.

    Returns:
        The packed protobuf action.
    """
    pb_action = pb_objects.Action()
    pb_action.mouseDx, pb_action.mouseDy = action["MOUSE"]
    for key, v in action.items():
        if key == "MOUSE":
            continue
        pb_action.keyEvents.append(
            pb_objects.KeyboardEvent(
                key=KEY_MAP[key],
                eventType=pb_objects.PRESS if v else pb_objects.RELEASE,
            ),
        )
    return pb_action


def start_minetest_server(
    minetest_path: str = "bin/minetest",
    config_path: str = "minetest.conf",
    log_path: str = "log/{}.log",
    server_port: int = 30000,
    world_dir: str = "newworld",
    sync_port: int = None,
    sync_dtime: float = 0.001,
    game_id: str = "minetest",
) -> subprocess.Popen:
    """Start a Minetest server.

    Args:
        minetest_path: Path to the Minetest executable.
        config_path: Path to the minetest.conf file.
        log_path: Path to the log files.
        server_port: Port of the server.
        world_dir: Path to the world directory.
        sync_port: Port for the synchronization with the server.
        sync_dtime: In-game time between two steps.
        game_id: Game ID of the game to be used.

    Returns:
        The server process.
    """
    cmd = [
        minetest_path,
        "--server",
        "--world",
        world_dir,
        "--gameid",
        game_id,
        "--config",
        config_path,
        "--port",
        str(server_port),
    ]
    if sync_port:
        cmd.extend(["--sync-port", str(sync_port)])
        cmd.extend(["--sync-dtime", str(sync_dtime)])
    stdout_file = log_path.format("server_stdout")
    stderr_file = log_path.format("server_stderr")

    with open(stdout_file, "w") as out, open(stderr_file, "w") as err:
        server_process = subprocess.Popen(cmd, stdout=out, stderr=err)
    return server_process


def start_minetest_client(
    minetest_path: str = "bin/minetest",
    config_path: str = "minetest.conf",
    log_path: str = "log/{}.log",
    client_port: int = 5555,
    server_port: int = 30000,
    cursor_img: str = "cursors/mouse_cursor_white_16x16.png",
    client_name: str = "MinetestAgent",
    sync_port: int = None,
    headless: bool = False,
    display: int = None,
) -> subprocess.Popen:
    """Start a Minetest client.

    Args:
        minetest_path: Path to the Minetest executable.
        config_path: Path to the minetest.conf file.
        log_path: Path to the log files.
        client_port: Port of the client.
        server_port: Port of the server to connect to.
        cursor_img: Path to the cursor image.
        client_name: Name of the client.
        sync_port: Port for the synchronization with the server.
        headless: Whether to run the client in headless mode.
        display: value of the DISPLAY variable.

    Returns:
        The client process.
    """
    cmd = [
        minetest_path,
        "--name",
        client_name,
        "--password",
        "1234",
        "--address",
        "0.0.0.0",  # listen to all interfaces
        "--port",
        str(server_port),
        "--go",
        "--dumb",
        "--client-address",
        "tcp://localhost:" + str(client_port),
        "--record",
        "--noresizing",
        "--config",
        config_path,
    ]
    if headless:
        # don't render to screen
        cmd.append("--headless")
    if cursor_img:
        cmd.extend(["--cursor-image", cursor_img])
    if sync_port:
        cmd.extend(["--sync-port", str(sync_port)])

    stdout_file = log_path.format("client_stdout")
    stderr_file = log_path.format("client_stderr")
    with open(stdout_file, "w") as out, open(stderr_file, "w") as err:
        client_env = os.environ.copy()
        if display is not None:
            client_env["DISPLAY"] = ":" + str(display)
        client_process = subprocess.Popen(cmd, stdout=out, stderr=err, env=client_env)
    return client_process


def start_xserver(
    display_idx: int = 1,
    display_size: Tuple[int, int] = (1024, 600),
    display_depth: int = 24,
) -> subprocess.Popen:
    """Start an X server.

    Args:
        display_idx: Value of the DISPLAY variable.
        display_size: Size of the display.
        display_depth: Depth of the display.

    Returns:
        The X server process.
    """
    cmd = [
        "Xvfb",
        f":{display_idx}",
        "-screen",
        "0",  # screennum param
        f"{display_size[0]}x{display_size[1]}x{display_depth}",
    ]
    xserver_process = subprocess.Popen(cmd)
    return xserver_process

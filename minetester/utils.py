"""Utility functions for Minetester."""
import os
import subprocess
import time
from tempfile import mkdtemp
from typing import Any, Dict, Optional, Tuple

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
    info = pb_obs.info
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
    minetest_path: str,
    config_path: str,
    log_path: str,
    client_port: int,
    server_port: int,
    cursor_img: str,
    client_name: str,
    media_cache_dir: str,
    sync_port: Optional[int] = None,
    dtime: Optional[float] = None,
    headless: bool = False,
    display: Optional[int] = None,
    set_gpu_vars: bool = True,
    set_vsync_vars: bool = True,
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
        media_cache_dir: Directory of minetest's media cache.
        sync_port: Port for the synchronization with the server.
        dtime: In-game time step in seconds.
        headless: Whether to run the client in headless mode.
        display: value of the DISPLAY variable.
        set_gpu_vars: whether to enable Nvidia GPU usage
        set_vsync_vars: whether to disable Vsync

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
        "--cache",
        media_cache_dir,
    ]
    if headless:
        # don't render to screen
        cmd.append("--headless")
    if cursor_img:
        cmd.extend(["--cursor-image", cursor_img])
    if sync_port:
        cmd.extend(["--sync-port", str(sync_port)])
    if dtime:
        cmd.extend(["--dtime", str(dtime)])

    stdout_file = log_path.format("client_stdout")
    stderr_file = log_path.format("client_stderr")
    with open(stdout_file, "w") as out, open(stderr_file, "w") as err:
        client_env = os.environ.copy()
        if display is not None:
            client_env["DISPLAY"] = ":" + str(display)
        if set_gpu_vars:
            # enable GPU usage
            client_env["__GLX_VENDOR_LIBRARY_NAME"] = "nvidia"
            client_env["__NV_PRIME_RENDER_OFFLOAD"] = "1"
        if set_vsync_vars:
            # disable vsync
            client_env["__GL_SYNC_TO_VBLANK"] = "0"
            client_env["vblank_mode"] = "0"
        client_process = subprocess.Popen(cmd, stdout=out, stderr=err, env=client_env)
    return client_process


def start_xserver(
    display_idx: int = 1,
    display_size: Tuple[int, int] = (1024, 600),
    display_depth: int = 24,
) -> subprocess.Popen:
    """Start a virtual framebuffer X server.

    Adapted from:
    https://github.com/man-group/pytest-plugins/blob/master/
    pytest-server-fixtures/pytest_server_fixtures/xvfb.py#L38

    Args:
        display_idx: Value of the DISPLAY variable.
        display_size: Size of the display.
        display_depth: Depth of the display.

    Returns:
        The X server process.

    Raises:
        RuntimeError: If X server fails to start or already exists.
    """
    display = f":{display_idx}"
    tmpdir = mkdtemp(prefix="XvfbServer.")
    cmd = [
        "Xvfb",
        display,
        "-fbdir",
        tmpdir,
        "-screen",
        "0",  # screennum param
        f"{display_size[0]}x{display_size[1]}x{display_depth}",
        "-nolisten",
        "tcp",
        "-reset",
        "-terminate",
    ]
    errfile = os.path.join(tmpdir, "Xvfb." + display + ".err")
    with open(errfile, "w") as f:  # use a file instead of a pipe to simplify polling
        xserver_process = subprocess.Popen(
            cmd,
            stderr=f,
            env=os.environ,
        )
        fbmem = os.path.join(tmpdir, "Xvfb_screen0")
        # Wait for Xvfb server to start
        while not os.path.exists(fbmem):
            if xserver_process.poll() is not None:
                break
            time.sleep(0.1)
        else:
            xserver_process.poll()
        if xserver_process.returncode is not None:
            with open(errfile) as f:
                err = f.read()
            already_active = "Server is already active for display"
            if already_active in err:
                raise RuntimeError(
                    already_active,
                    xserver_process.returncode,
                    err,
                )
            else:
                raise RuntimeError(
                    "Failed to start Xvfb server",
                    xserver_process.returncode,
                    err,
                )
    return xserver_process


def read_config_file(file_path: os.PathLike):
    """Read and parse minetest config files.

    Args:
        file_path: Path to minetest config.

    Returns:
        dictionary containing the parsed config.
    """
    config = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if value.isdigit():
                    value = int(value)
                elif value.replace(".", "", 1).isdigit():
                    value = float(value)
                elif value.lower() == "true":
                    value = True
                elif value.lower() == "false":
                    value = False
                config[key] = value
    return config


def write_config_file(file_path: os.PathLike, config: Dict[str, Any]):
    """Write a minetest config file.

    Args:
        file_path: Write path for minetest config.
        config: Dictionary representing minetest config.

    """
    with open(file_path, "w") as f:
        for key, value in config.items():
            f.write(f"{key} = {value}\n")

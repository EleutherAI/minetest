import os
import time
import json
import cv2
import zmq
import numpy as np
from minetester.utils import unpack_pb_obs

class DataRecorder:
    def __init__(
        self,
        data_path: os.PathLike,
        target_address: str,
        timeout: int = 1000,
        max_queue_length: int = 1200,
        max_attempts: int = 10,
        debug: bool = False,
        subsample_rate: int = 1,  # new argument for subsampling rate
    ):
        self.target_address = target_address
        self.data_path = data_path
        self.timeout = timeout
        self.max_queue_length = max_queue_length
        self.max_attempts = max_attempts
        self.debug = debug
        self.subsample_rate = subsample_rate  # subsampling rate
        self._recording = False

        # Setup ZMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.RCVTIMEO = self.timeout
        self.socket.connect(f"tcp://{self.target_address}")

        # Subscribe to all topics
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")

        # Set maximum message queue length (high water mark)
        self.socket.setsockopt(zmq.RCVHWM, self.max_queue_length)

        # Set timeout in milliseconds
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)

        # Create data directory if it doesn't exist
        os.makedirs(self.data_path, exist_ok=True)

        # Prepare paths for video and action log
        self.video_path = os.path.join(self.data_path, "video.avi")
        self.action_log_path = os.path.join(self.data_path, "actions.jsonl")

        # Initialize video writer
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video_writer = cv2.VideoWriter(self.video_path, self.fourcc, 20.0, (1024, 600))

    def start(self):
        with open(self.action_log_path, "w") as action_log:
            self._recording = True
            num_attempts = 0
            frame_count = 0  # count frames for subsampling

            while self._recording:
                try:
                    # Receive data
                    raw_data = self.socket.recv()
                    num_attempts = 0

                    # Subsample based on the specified rate
                    if frame_count % self.subsample_rate == 0:
                        obs, rew, terminal, info, action = unpack_pb_obs(raw_data)

                        if self.debug:
                            print(obs, type(obs))
                            action_str = ""
                            for key in action.keys():
                                if key != "MOUSE" and action[key]:
                                    action_str += key + ", "
                            print(f"action={action_str}, rew={rew}, T?={terminal}")

                        # Write frame to video
                        self.video_writer.write(cv2.cvtColor(np.array(obs), cv2.COLOR_RGB2BGR))

                        # Write action to action log (one line per frame)
                        action_log.write(json.dumps(action) + "\n")

                    frame_count += 1
                except zmq.ZMQError as err:
                    if err.errno == zmq.EAGAIN:
                        print(f"Reception attempts: {num_attempts}")
                        if num_attempts >= self.max_attempts:
                            print("Session finished.")
                            self._recording = False
                        num_attempts += 1
                    else:
                        print(f"ZMQError: {err}")
                        self._recording = False

    def stop(self):
        self._recording = False
        self.video_writer.release()  # release video writer


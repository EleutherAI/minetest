import subprocess
import sys
import argparse
from minetester.data_recorder import DataRecorder
import multiprocessing

def run_data_recorder(debug, data_dir):
    # Start recorder
    address = "localhost:5555"
    num_attempts = 10
    recorder = DataRecorder(data_dir, address, max_attempts=num_attempts, debug=debug)
    recorder.start()  # warning: file quickly grows very large

def run_minetest():
    command = [
        "bin/minetest",
        "--name", "MinetestAgent",
        "--password", "password",
        #"--address", "0.0.0.0",
        #"--port", "30000",
        "--go",
        "--client-address", "tcp://*:5555",
        "--record",
        "--noresizing",
        "--cursor-image", "cursors/mouse_cursor_white_16x16.png",
        "--config", "scripts/minetest.conf",
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{' '.join(command)}' failed with return code {e.returncode}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Launch data recorder and minetest.')
    parser.add_argument('--debug', action='store_true', help='If set, data is not written')
    parser.add_argument('--data_dir', type=str, default="user_recording", help='Directory for data recording')
    args = parser.parse_args()
    
    process = multiprocessing.Process(target=run_minetest)
    
    process.start()
    run_data_recorder(args.debug, args.data_dir)
    process.join()

if __name__ == "__main__":
    main()

import subprocess
import signal
import os
import config

config.read_command_line()


# Function to start a process
def start_process(command):
    return subprocess.Popen(command, shell=True, executable='/bin/bash')


# Function to stop a process
def stop_process(process):
    if process:
        os.kill(process.pid, signal.SIGTERM)


# Path to the virtual environment
venv_path = ".venv"  # Replace with the path to your virtual environment

manager_command = f"source {venv_path}/bin/activate && python3 manager.py"
manager_process = start_process(manager_command)

game_command = f"source {venv_path}/bin/activate && python3 game.py"
game_process = start_process(game_command)

# Wait for the game process to finish
game_process.wait()

# Stop the image generation script
stop_process(manager_process)

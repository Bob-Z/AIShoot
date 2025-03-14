import subprocess
import time
import signal
import os
import shutil

# Function to start a process
def start_process(command):
    return subprocess.Popen(command, shell=True, executable='/bin/bash')

# Function to stop a process
def stop_process(process):
    if process:
        os.kill(process.pid, signal.SIGTERM)

# Path to the virtual environment
venv_path = "venv"  # Replace with the path to your virtual environment

# Directory to load generated images and music
image_dir = "generated_images"
music_dir = "generated_music"

# Always start the image generation script
activate_venv_command_images = f"source {venv_path}/bin/activate && python3 generate_images.py"
image_gen_process = start_process(activate_venv_command_images)

# Always start the music generation script
activate_venv_command_music = f"source {venv_path}/bin/activate && python3 generate_music.py"
music_gen_process = start_process(activate_venv_command_music)

# Wait for the flag file to be created, indicating that initial images are generated
flag_file = os.path.join(image_dir, "initial_images_generated.flag")
while not os.path.exists(flag_file):
    time.sleep(1)

# Activate the virtual environment and start the main game script
game_command = f"source {venv_path}/bin/activate && python3 game.py"
game_process = start_process(game_command)

# Wait for the game process to finish
game_process.wait()

# Stop the image generation script
stop_process(image_gen_process)

# Stop the music generation script
stop_process(music_gen_process)


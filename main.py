import subprocess
import time
import signal
import os
import shutil
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

image_dir = "generated_image"
music_dir = "generated_music"
sound_dir = "generated_sound"

# Clear the generated files directory
if config.data['fast_start'] is False:
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
    os.makedirs(image_dir, exist_ok=True)

    if os.path.exists(music_dir):
        shutil.rmtree(music_dir)
    os.makedirs(music_dir, exist_ok=True)

    if os.path.exists(sound_dir):
        shutil.rmtree(sound_dir)
    os.makedirs(sound_dir, exist_ok=True)

    # Activate the virtual environment and start the sound generation script
    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_sound.py"
    sound_gen_process = start_process(activate_venv_command)
    sound_gen_process.wait()

    # Activate the virtual environment and start the music generation script
    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_music.py"
    music_gen_process = start_process(activate_venv_command)
    music_gen_process.wait()

# Activate the virtual environment and start the image generation script
activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_images.py"
image_gen_process = start_process(activate_venv_command)

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

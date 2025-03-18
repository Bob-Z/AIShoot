import subprocess
import time
import signal
import os
import config
import shutil
import json


# Function to start a process
def start_process(command):
    return subprocess.Popen(command, shell=True, executable='/bin/bash')


# Function to stop a process
def stop_process(process):
    if process:
        os.kill(process.pid, signal.SIGTERM)


config.read_command_line()

# Path to the virtual environment
venv_path = ".venv"  # Replace with the path to your virtual environment

# Clear the generated files directory
if config.data['fast_start'] is False:
    if os.path.exists(config.data["image_dir"]):
        shutil.rmtree(config.data["image_dir"])

    if os.path.exists(config.data["music_dir"]):
        shutil.rmtree(config.data["music_dir"])

    if os.path.exists(config.data["sound_dir"]):
        shutil.rmtree(config.data["sound_dir"])

os.makedirs(config.data["image_dir"], exist_ok=True)
os.makedirs(config.data["music_dir"], exist_ok=True)
os.makedirs(config.data["sound_dir"], exist_ok=True)

# Activate the virtual environment and start the music generation script
# activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_music.py"
# music_gen_process = start_process(activate_venv_command)
# music_gen_process.wait()

bg_idx = 0

print("Generating initial images")
data = {
    "file_list": [
        {"prompt": config.data["background_prompt"][bg_idx%len(config.data["background_prompt"])],
         "filename": os.path.join(config.data['image_dir'], config.data['background_filename'] + "0.png")},
        {"prompt": config.data["player_sprite_prompt"],
         "filename": os.path.join(config.data['image_dir'], config.data['player_sprite_filename'])},
        {"prompt": config.data["bullet_sprite_prompt"],
         "filename": os.path.join(config.data['image_dir'], config.data['bullet_sprite_filename'])},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_images.py"
image_gen_process = start_process(activate_venv_command)
image_gen_process.wait()

explosion_sound_idx = 0

print("Generating initial sounds")
data = {
    "file_list": [
        {"prompt": config.data["bullet_sound_prompt"],
         "filename": os.path.join(config.data['sound_dir'], config.data['bullet_sound_filename'])},
        {"prompt": config.data["explosion_sound_prompt"][
            explosion_sound_idx % len(config.data["explosion_sound_prompt"])],
         "filename": os.path.join(config.data['sound_dir'], config.data['explosion_sound_filename'] + str(explosion_sound_idx))},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_sound.py"
image_gen_process = start_process(activate_venv_command)
image_gen_process.wait()

explosion_sound_idx += 1

enemy_image_idx = 0

while True:
    # Generate new images
    data = {
        "file_list": [
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx%len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename'] + str(enemy_image_idx) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx%len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename'] + str(enemy_image_idx + 1) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx%len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename'] + str(enemy_image_idx + 2) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx%len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename'] + str(enemy_image_idx + 3) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx%len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename'] + str(enemy_image_idx + 4) + ".png")},

            {"prompt": config.data["background_prompt"][bg_idx%len(config.data["background_prompt"])],
             "filename": os.path.join(config.data['image_dir'], config.data['background_filename'] + str(bg_idx) + ".png")},
        ]
    }

    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_images.py"
    image_gen_process = start_process(activate_venv_command)
    image_gen_process.wait()

    enemy_image_idx += 5
    bg_idx += 1

    # Generate new sounds
    data = {
        "file_list": [
            {"prompt": config.data["explosion_sound_prompt"][explosion_sound_idx%len(config.data["explosion_sound_prompt"])],
             "filename": os.path.join(config.data['sound_dir'], config.data['explosion_sound_filename'] + str(explosion_sound_idx))},
        ]
    }

    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_sound.py"
    sound_gen_process = start_process(activate_venv_command)
    sound_gen_process.wait()

    explosion_sound_idx += 1

# Always start the image generation script
# generate_image_script = f"source {venv_path}/bin/activate && python3 generate_images.py"
# image_gen_process = start_process(generate_image_script)

# Always start the music generation script
# activate_venv_command_music = f"source {venv_path}/bin/activate && python3 generate_music.py"
# music_gen_process = start_process(activate_venv_command_music)

# Wait for the flag file to be created, indicating that initial images are generated
# flag_file = os.path.join(image_dir, "initial_images_generated.flag")
# while not os.path.exists(flag_file):
#    time.sleep(1)

# Activate the virtual environment and start the main game script
# game_command = f"source {venv_path}/bin/activate && python3 game.py"
# game_process = start_process(game_command)

# Wait for the game process to finish
# game_process.wait()

# Stop the image generation script
# stop_process(image_gen_process)

# Stop the music generation script
# stop_process(music_gen_process)

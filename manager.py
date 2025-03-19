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

    if os.path.exists(config.data["tmp_dir"]):
        shutil.rmtree(config.data["tmp_dir"])

os.makedirs(config.data["image_dir"], exist_ok=True)
os.makedirs(config.data["music_dir"], exist_ok=True)
os.makedirs(config.data["sound_dir"], exist_ok=True)
os.makedirs(config.data["tmp_dir"], exist_ok=True)

bg_idx = 0

print("Generating initial images")
data = {
    "file_list": [
        {"prompt": config.data["background_prompt"][bg_idx % len(config.data["background_prompt"])],
         "filename": os.path.join(config.data['image_dir'], config.data['background_filename'] + "0.png")},
        {"prompt": config.data["player_sprite_prompt"],
         "filename": os.path.join(config.data['tmp_dir'], config.data['player_sprite_filename'])},
        {"prompt": config.data["bullet_sprite_prompt"],
         "filename": os.path.join(config.data['tmp_dir'], config.data['bullet_sprite_filename'])},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_image.py"
image_gen_process = start_process(activate_venv_command)
image_gen_process.wait()

print("Removing background of initial images")
data = {
    "file_list": [
        {"input_filename": os.path.join(config.data['tmp_dir'], config.data['player_sprite_filename']),
         "output_filename": os.path.join(config.data['image_dir'], config.data['player_sprite_filename'])},
        {"input_filename": os.path.join(config.data['tmp_dir'], config.data['bullet_sprite_filename']),
         "output_filename": os.path.join(config.data['image_dir'], config.data['bullet_sprite_filename'])},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 remove_bg.py"
remove_bg_process = start_process(activate_venv_command)
remove_bg_process.wait()

print("Generating initial sounds")

explosion_sound_idx = 0

data = {
    "file_list": [
        {"prompt": config.data["bullet_sound_prompt"],
         "filename": os.path.join(config.data['sound_dir'], config.data['bullet_sound_filename'])},
        {"prompt": config.data["explosion_sound_prompt"][
            explosion_sound_idx % len(config.data["explosion_sound_prompt"])],
         "filename": os.path.join(config.data['sound_dir'],
                                  config.data['explosion_sound_filename'] + str(explosion_sound_idx))},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_sound.py"
sound_gen_process = start_process(activate_venv_command)
sound_gen_process.wait()

explosion_sound_idx += 1

print("Generating initial music")
music_idx = 0
data = {
    "file_list": [
        {"prompt": config.data["music_prompt"][
            music_idx % len(config.data["music_prompt"])],
         "filename": os.path.join(config.data['music_dir'], config.data['music_filename'] + str(music_idx))},
    ]
}
with open("list.json", "w") as write:
    json.dump(data, write)

activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_music.py"
music_gen_process = start_process(activate_venv_command)
music_gen_process.wait()

music_idx += 1

enemy_image_idx = 0

while True:
    # Generate new images
    data = {
        "file_list": [
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx % len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['tmp_dir'],
                                      config.data['enemy_sprite_filename'] + str(enemy_image_idx) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx % len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['tmp_dir'],
                                      config.data['enemy_sprite_filename'] + str(enemy_image_idx + 1) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx % len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['tmp_dir'],
                                      config.data['enemy_sprite_filename'] + str(enemy_image_idx + 2) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx % len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['tmp_dir'],
                                      config.data['enemy_sprite_filename'] + str(enemy_image_idx + 3) + ".png")},
            {"prompt": config.data["enemy_sprite_prompt"][enemy_image_idx % len(config.data["enemy_sprite_prompt"])],
             "filename": os.path.join(config.data['tmp_dir'],
                                      config.data['enemy_sprite_filename'] + str(enemy_image_idx + 4) + ".png")},

            {"prompt": config.data["background_prompt"][bg_idx % len(config.data["background_prompt"])],
             "filename": os.path.join(config.data['image_dir'],
                                      config.data['background_filename'] + str(bg_idx) + ".png")},
        ]
    }

    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_image.py"
    image_gen_process = start_process(activate_venv_command)
    image_gen_process.wait()

    # Remove sprites backgrounds
    data = {
        "file_list": [
            {"input_filename": os.path.join(config.data['tmp_dir'], config.data['enemy_sprite_filename']) + str(
                enemy_image_idx + 0) + ".png",
             "output_filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename']) + str(
                 enemy_image_idx + 0) + ".png"},
            {"input_filename": os.path.join(config.data['tmp_dir'], config.data['enemy_sprite_filename']) + str(
                enemy_image_idx + 1) + ".png",
             "output_filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename']) + str(
                 enemy_image_idx + 1) + ".png"},
            {"input_filename": os.path.join(config.data['tmp_dir'], config.data['enemy_sprite_filename']) + str(
                enemy_image_idx + 2) + ".png",
             "output_filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename']) + str(
                 enemy_image_idx + 2) + ".png"},
            {"input_filename": os.path.join(config.data['tmp_dir'], config.data['enemy_sprite_filename']) + str(
                enemy_image_idx + 3) + ".png",
             "output_filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename']) + str(
                 enemy_image_idx + 3) + ".png"},
            {"input_filename": os.path.join(config.data['tmp_dir'], config.data['enemy_sprite_filename']) + str(
                enemy_image_idx + 4) + ".png",
             "output_filename": os.path.join(config.data['image_dir'], config.data['enemy_sprite_filename']) + str(
                 enemy_image_idx + 4) + ".png"}
        ]
    }
    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 remove_bg.py"
    remove_bg_process = start_process(activate_venv_command)
    remove_bg_process.wait()

    enemy_image_idx += 5
    bg_idx += 1

    # Generate new sounds
    data = {
        "file_list": [
            {"prompt": config.data["explosion_sound_prompt"][
                explosion_sound_idx % len(config.data["explosion_sound_prompt"])],
             "filename": os.path.join(config.data['sound_dir'],
                                      config.data['explosion_sound_filename'] + str(explosion_sound_idx))},
        ]
    }

    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_sound.py"
    sound_gen_process = start_process(activate_venv_command)
    sound_gen_process.wait()

    explosion_sound_idx += 1

    # Generate new musics
    data = {
        "file_list": [
            {"prompt": config.data["music_prompt"][music_idx % len(config.data["music_prompt"])],
             "filename": os.path.join(config.data['music_dir'], config.data['music_filename'] + str(music_idx))},
        ]
    }

    with open("list.json", "w") as write:
        json.dump(data, write)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_music.py"
    music_gen_process = start_process(activate_venv_command)
    music_gen_process.wait()

    music_idx += 1

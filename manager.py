import subprocess
import signal
import os
import config
import shutil
import json
import time

bark_voices = ["v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2", "v2/en_speaker_3", "v2/en_speaker_4",
               "v2/en_speaker_5", "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", "v2/en_speaker_9"]


# Function to start a process
def start_process(command):
    return subprocess.Popen(command, shell=True, executable='/bin/bash')


# Function to stop a process
def stop_process(process):
    if process:
        os.kill(process.pid, signal.SIGTERM)


def generate_initial_resources():
    global bg_idx
    global explosion_sound_idx

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
    generate_new_musics()


def generate_new_images():
    global enemy_image_idx
    global bg_idx

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


def generate_new_taunts():
    global taunt_system_idx
    global taunt_user_idx
    global txt_idx

    # Generate text
    filename = os.path.join(config.data['text_dir'], config.data['taunt_filename'] + str(txt_idx) + ".txt")
    data = {
        "file_list": [
            {"filename": filename,
             "prompt": [
                 {
                     "role": "system",
                     "content": config.data["taunt_system_prompt"][
                         taunt_system_idx % len(config.data["taunt_system_prompt"])]
                 },
                 {"role": "user", "content": config.data["taunt_user_prompt"][
                     taunt_user_idx % len(config.data["taunt_user_prompt"])]}
             ]
             }
        ]
    }

    with open("list.json", "w") as list_json:
        json.dump(data, list_json)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_text.py"
    text_gen_process = start_process(activate_venv_command)
    text_gen_process.wait()

    # Generate vocal
    taunt_txt = ""
    with open(filename, "r") as taunt_txt_file:
        taunt_txt = taunt_txt_file.read()

    data = {
        "file_list": [
            {"filename": os.path.join(config.data['vocal_dir'],
                                      config.data['taunt_filename'] + str(txt_idx) + ".wav"),
             "text": taunt_txt,
             "voice": bark_voices[txt_idx % len(bark_voices)],
             }
        ]
    }

    with open("list.json", "w") as list_json:
        json.dump(data, list_json)

    activate_venv_command = f"source {venv_path}/bin/activate && python3 generate_vocal.py"
    vocal_gen_process = start_process(activate_venv_command)
    vocal_gen_process.wait()

    taunt_system_idx += 1
    taunt_user_idx += 1
    txt_idx += 1


def generate_new_sounds():
    global explosion_sound_idx
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


def generate_new_musics():
    global music_idx

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


config.read_command_line()

# Path to the virtual environment
venv_path = ".venv"  # Replace with the path to your virtual environment

# Clear the generated files directory
if config.data['reset_all_media'] is True:
    if os.path.exists(config.data["image_dir"]):
        shutil.rmtree(config.data["image_dir"])

    if os.path.exists(config.data["music_dir"]):
        shutil.rmtree(config.data["music_dir"])

    if os.path.exists(config.data["sound_dir"]):
        shutil.rmtree(config.data["sound_dir"])

    if os.path.exists(config.data["text_dir"]):
        shutil.rmtree(config.data["text_dir"])

    if os.path.exists(config.data["vocal_dir"]):
        shutil.rmtree(config.data["vocal_dir"])

    if os.path.exists(config.data["tmp_dir"]):
        shutil.rmtree(config.data["tmp_dir"])

os.makedirs(config.data["image_dir"], exist_ok=True)
os.makedirs(config.data["music_dir"], exist_ok=True)
os.makedirs(config.data["sound_dir"], exist_ok=True)
os.makedirs(config.data["text_dir"], exist_ok=True)
os.makedirs(config.data["vocal_dir"], exist_ok=True)
os.makedirs(config.data["tmp_dir"], exist_ok=True)

explosion_sound_idx = 0
music_idx = 0
bg_idx = 0
enemy_image_idx = 0
taunt_system_idx = 0
taunt_user_idx = 0
txt_idx = 0

generate_initial_resources()

while True:
    start = time.time()
    generate_new_images()
    end = time.time()
    print(f"New images generated in {end - start} seconds")

    start = time.time()
    generate_new_taunts()
    end = time.time()
    print(f"New taunts generated in {end - start} seconds")

    start = time.time()
    generate_new_sounds()
    end = time.time()
    print(f"New sounds generated in {end - start} seconds")

    start = time.time()
    generate_new_musics()
    end = time.time()
    print(f"New musics generated in {end - start} seconds")

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import config
import json
import os

with open("list.json", "r") as file:
    input_file = json.load(file)

config.read_command_line()

model = MusicGen.get_pretrained("facebook/musicgen-medium")
model.set_generation_params(duration=config.data['music_duration'])

descriptions = []
for f in input_file["file_list"]:
    descriptions.append(f["prompt"])

wav = model.generate(descriptions)  # generates all sample

for idx, (one_wav, one_input) in enumerate(zip(wav, input_file["file_list"])):
    audio_write("tmp", one_wav.cpu(), model.sample_rate, strategy="loudness")
    os.rename("tmp.wav", one_input["filename"] + ".wav")  # Avoid game engine to read a file while it is not entirely written on the disk

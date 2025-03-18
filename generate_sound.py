from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write
import os
import json

with open("list.json", "r") as file:
    input_file = json.load(file)

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=3)  # generate 3 seconds.

for d in input_file["file_list"]:
    print(f'Generating sound {d["filename"]} with prompt: {d["prompt"]}')
    descriptions = [d["prompt"]]
    wav = model.generate(descriptions)  # generates 1 samples.
    audio_write("tmp", wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
    os.rename("tmp.wav", d["filename"] + ".wav")  # Avoid game engine to read a file while it is not entirely written on the disk
